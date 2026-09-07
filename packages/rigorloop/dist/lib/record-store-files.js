// Shared filesystem boundary for the unadopted explicit recorder.
import * as fs from "node:fs";
import { resolve, join, dirname, basename } from "node:path";
import { createHash, randomBytes } from "node:crypto";

export const MIB = 1024 * 1024;
export const digest = bytes => bytes === null ? null : `sha256:${createHash("sha256").update(bytes).digest("hex")}`;
export function stop(code) { throw Object.assign(new Error(code), {recordStoreCode:code}); }
const same = (a,b) => a.dev === b.dev && a.ino === b.ino;
function stat(path) { try { return fs.lstatSync(path); } catch(e) { if(e.code === "ENOENT") return null; throw e; } }

export class RecordFiles {
  constructor(root) {
    this.root = resolve(root);
    this.identity = stat(this.root);
    if (!this.identity?.isDirectory() || this.identity.isSymbolicLink()) stop("unsafe-path");
  }
  path(path) {
    if (typeof path !== "string" || !/^[\x20-\x7e]+$/.test(path) || path.length > 1024 || path.includes("\\") || /^[A-Za-z]:/.test(path) || path.split("/").some(p=>!p || p === "." || p === "..")) stop("unsafe-path");
    return join(this.root,path);
  }
  inspect(path, directory=false) {
    const target=this.path(path), chain=[[this.root,this.identity]];
    let cursor=this.root;
    const parts=path.split("/");
    for (let i=0;i<parts.length;i++) {
      cursor=join(cursor,parts[i]); const info=stat(cursor);
      if (!info) return {target,info:null,chain};
      if (info.isSymbolicLink() || (i < parts.length-1 || directory ? !info.isDirectory() : !info.isFile() || info.nlink !== 1)) stop("unsafe-path");
      chain.push([cursor,info]);
    }
    this.assert(chain);
    return {target,info:chain.at(-1)[1],chain};
  }
  assert(chain) {
    for (const [path,identity] of chain) {
      const actual=stat(path);
      if (!actual || actual.isSymbolicLink() || !same(actual,identity)) stop("unsafe-path");
    }
  }
  read(path,limit=MIB,hashOnly=false) {
    const item=this.inspect(path);
    if (!item.info) { this.assert(item.chain); return null; }
    if (!hashOnly && item.info.size > limit) stop("limit-exceeded");
    const fd=fs.openSync(item.target,fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW | fs.constants.O_NONBLOCK);
    try {
      const opened=fs.fstatSync(fd);
      if (!opened.isFile() || opened.nlink !== 1 || !same(opened,item.info)) stop("unsafe-path");
      this.assert(item.chain);
      const hash=createHash("sha256"), chunks=[], buffer=Buffer.alloc(64*1024);
      let count=0, n;
      while ((n=fs.readSync(fd,buffer,0,buffer.length,null)) > 0) {
        count+=n; if (!hashOnly && count > limit) stop("limit-exceeded");
        if (hashOnly) hash.update(buffer.subarray(0,n)); else chunks.push(Buffer.from(buffer.subarray(0,n)));
      }
      const after=fs.fstatSync(fd);
      this.assert(item.chain);
      if (opened.size !== after.size || opened.mtimeMs !== after.mtimeMs || opened.ctimeMs !== after.ctimeMs) stop("identity-conflict");
      return hashOnly ? `sha256:${hash.digest("hex")}` : Buffer.concat(chunks);
    } finally { fs.closeSync(fd); }
  }
  hash(path) { return this.read(path,Infinity,true); }
  withParent(item,action) {
    const parents=item.chain.filter(([p])=>p!==item.target), parent=dirname(item.target);
    if(parents.at(-1)?.[0]!==parent) stop("unsafe-path");
    this.assert(parents);
    const cwd=process.cwd();
    try {
      // This synchronous section never yields. The working directory pins the
      // verified parent inode; single basenames cannot follow a replaced ancestor.
      process.chdir(parent);
      const opened=stat(".");
      if(!opened?.isDirectory() || !same(opened,parents.at(-1)[1])) stop("unsafe-path");
      this.assert(parents);
      const result=action(basename(item.target));
      this.assert(parents);
      const fd=fs.openSync(".",fs.constants.O_RDONLY|fs.constants.O_NOFOLLOW);
      try { fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
      return result;
    } finally { process.chdir(cwd); }
  }
  sync(path) {
    const item=path===null?{target:this.root,info:this.identity,chain:[[this.root,this.identity]]}:this.inspect(path,true);
    if(!item.info) stop("unsafe-path");
    const fd=fs.openSync(item.target,fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW);
    try { this.assert(item.chain); fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
  }
  mkdir(path) {
    const item=this.inspect(path,true);
    if(item.info) return false;
    this.withParent(item,name=>fs.mkdirSync(name,{mode:0o700}));
    return true;
  }
  write(path,bytes,{exclusive=false,expected}={}) {
    const item=this.inspect(path);
    this.assert(item.chain);
    if (expected !== undefined && this.hash(path) !== expected) stop("identity-conflict");
    this.withParent(item,name=>{
    if(exclusive) {
      const fd=fs.openSync(name,fs.constants.O_WRONLY|fs.constants.O_CREAT|fs.constants.O_EXCL|fs.constants.O_NOFOLLOW,0o600);
      try { this.assert(item.chain); fs.writeFileSync(fd,bytes); fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
    } else {
      const temporary=`.record-store-${randomBytes(16).toString("hex")}`;
      const fd=fs.openSync(temporary,"wx",0o600);
      try {
        this.assert(item.chain); fs.writeFileSync(fd,bytes); fs.fsyncSync(fd);
        this.assert(item.chain);
        if (expected !== undefined && this.hash(path) !== expected) stop("identity-conflict");
        fs.renameSync(temporary,name);
        // Parent identities must still be the ones validated before publication.
        this.assert(item.chain.filter(([p])=>p !== item.target));
      } finally {
        fs.closeSync(fd);
        if(stat(temporary)) fs.unlinkSync(temporary);
      }
    }
    });
  }
  remove(path,expected) {
    const item=this.inspect(path); if(!item.info) return;
    this.assert(item.chain);
    if(this.hash(path) !== expected) stop("identity-conflict");
    this.withParent(item,name=>fs.unlinkSync(name));
  }
  removeDirectory(path,identity) {
    const item=this.inspect(path,true); if(!item.info) return;
    if(`${item.info.dev}:${item.info.ino}` !== identity) stop("recovery-needed");
    this.assert(item.chain);
    try { this.withParent(item,name=>fs.rmdirSync(name)); }
    catch(e) { if(e.code !== "ENOTEMPTY" && e.code !== "EEXIST") throw e; }
  }
}
