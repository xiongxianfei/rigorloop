// Internal native Node collection/receipt adapter. The Python executor owns scheduling.
import * as native from 'node:test';
import {registerHooks} from 'node:module';
import {AsyncLocalStorage} from 'node:async_hooks';
import {mkdirSync, readFileSync, writeFileSync, renameSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {dirname, resolve} from 'node:path';
import {fileURLToPath} from 'node:url';
import {inspect} from 'node:util';

const self = fileURLToPath(import.meta.url);
const collectionRoot = process.env.RIGORLOOP_NODE_COLLECTION;
const ancestry = new AsyncLocalStorage();
const declarations = [];
function save(path, value) {
  mkdirSync(dirname(path), {recursive:true});
  writeFileSync(path+'.pending', JSON.stringify(value)+'\n');
  renameSync(path+'.pending',path);
}
function parameters(name, options, fn) {
  if (typeof options === 'function') { fn=options; options={}; }
  if (typeof name !== 'string' || !name.trim() || name.includes('\n') || name.includes('\0'))
    throw Error('Node cases require explicit nonempty single-line names');
  if (options != null && typeof options !== 'object') throw Error('unsupported Node test options');
  if (options?.concurrency && options.concurrency !== 1)
    throw Error('nested Node test concurrency exceeds one case allocation');
  if (typeof fn !== 'function' && !options?.todo) throw Error('Node case has no body');
  return [options ?? {},fn];
}
export function collectTest(name, options, fn) {
  [options,fn]=parameters(name,options,fn);
  const id=[...(ancestry.getStore() ?? []),name].join(' ');
  if (declarations.includes(id)) throw Error('duplicate or ambiguous Node case: '+id);
  declarations.push(id);
  // Execute declarations through the native loader; collection never runs bodies/hooks.
  return native.test(name,{...options,skip:true},()=>{});
}
export function collectSuite(name, options, fn) {
  [options,fn]=parameters(name,options,fn);
  return native.describe(name,options, (...args)=>ancestry.run(
    [...(ancestry.getStore() ?? []),name],()=>fn(...args)));
}
for (const wrapper of [collectTest,collectSuite]) {
  for (const flag of ['skip','todo','only']) wrapper[flag]=(name,options,fn)=>{
    if (typeof options==='function') {fn=options;options={};}
    return wrapper(name,{...options,[flag]:true},fn ?? (()=>{}));
  };
}
export function collectHook() {}

// Imported only into collection children. Both default and named native imports
// are instrumented; ordinary execution uses the untouched node:test module.
if (collectionRoot) {
  const exports = `export * from 'node:test'; export {collectTest as default, collectTest as test, collectTest as it, collectSuite as describe, collectSuite as suite, collectHook as before, collectHook as after, collectHook as beforeEach, collectHook as afterEach} from ${JSON.stringify(import.meta.url)};`;
  const wrapper='data:text/javascript,'+encodeURIComponent(exports);
  registerHooks({resolve(specifier, context, next) {
    if (specifier==='node:test' && context.parentURL!==wrapper && context.parentURL!==import.meta.url)
      return {url:wrapper,shortCircuit:true};
    return next(specifier,context);
  }});
  process.on('exit',code=>{
    if (code===0) save(resolve(collectionRoot,createHash('sha256').update(resolve(process.argv[1])).digest('hex')+'.json'),
      {file:resolve(process.argv[1]),ids:declarations});
  });
}

async function main(mode, destination, scopeText, expected) {
  if (!['collect','case','observe'].includes(mode)) throw Error('unknown Node adapter mode');
  const scope=JSON.parse(scopeText);
  if (Object.keys(scope).some(k=>!['files','cwd','globPatterns'].includes(k))) throw Error('unknown Node discovery scope');
  const startedAt=Number(process.hrtime.bigint())/1e9;
  if (scope.cwd) process.chdir(scope.cwd);
  const options={...scope,concurrency:1};
  delete options.cwd;
  const files=new Set();
  if (mode==='collect') {
    options.execArgv=['--import',self];
    // run() copies the process environment into isolated native children.
    process.env.RIGORLOOP_NODE_COLLECTION=destination+'.declarations';
  } else if (mode==='case') {
    if (!expected) throw Error('missing required Node case');
    options.testNamePatterns=[new RegExp('^'+expected.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'$')];
  }
  const names=[],skipped=[],stack=[],starts=[],suites=new Set();
  let failed=false,summary;
  for await (const event of native.run(options)) {
    const d=event.data;
    if (event.type==='test:enqueue' && d.file && resolve(d.file)===resolve(d.name)) files.add(resolve(d.file));
    if (event.type==='test:stdout') process.stdout.write(d.message);
    if (event.type==='test:stderr') process.stderr.write(d.message);
    if (event.type==='test:start') {
      stack.length=d.nesting;stack[d.nesting]=d.name;
      if (!(d.file && resolve(d.file)===resolve(d.name))) starts.push(stack.join(' '));
    }
    if (event.type==='test:pass' || event.type==='test:fail') {
      if (d.details.type==='suite') suites.add([...stack.slice(0,d.nesting),d.name].join(' '));
      if (d.details.type!=='suite' && !(d.file && resolve(d.file)===resolve(d.name))) {
        const id=[...stack.slice(0,d.nesting),d.name].join(' ');
        names.push(id);
        if (d.skip || d.todo) skipped.push(id);
      }
      if (event.type==='test:fail') {failed=true;process.stderr.write(inspect(d,{depth:5})+'\n');}
    }
    if (event.type==='test:summary' && !d.file) summary=d;
  }
  delete process.env.RIGORLOOP_NODE_COLLECTION;
  if (!summary) throw Error('native Node run lacks final summary');
  if (failed || !summary.success) {process.exitCode=1;return;}
  if (mode==='collect') {
    const groups=[];
    for (const file of files) {
      const path=resolve(destination+'.declarations',createHash('sha256').update(file).digest('hex')+'.json');
      const data=JSON.parse(readFileSync(path,'utf8'));
      if (data.file!==file || !Array.isArray(data.ids) || !data.ids.length)
        throw Error('zero or invalid Node case declarations: '+file);
      groups.push(data);
    }
    if (!groups.length) throw Error('zero Node test files');
    save(destination,{mode:'collect',groups});
  } else {
    const counts=summary.counts;
    const started=starts.filter(id=>!suites.has(id));
    const successful=names.length>0 && new Set(names).size===names.length && skipped.length===0 &&
      JSON.stringify(started)===JSON.stringify(names) && counts.tests===names.length && counts.passed===names.length &&
      counts.failed===0 && counts.cancelled===0 && counts.skipped===0 && counts.todo===0 &&
      (mode!=='case' || (names.length===1 && names[0]===expected));
    save(destination,{mode,discovered:names,started,completed:names,
      tests_run:names.length,skipped,successful,started_at:startedAt,completed_at:Number(process.hrtime.bigint())/1e9});
    if (!successful) throw Error('required Node case receipt is zero, extra, skipped, todo or incomplete');
  }
}
if (!collectionRoot && resolve(process.argv[1] ?? '')===self) {
  main(...process.argv.slice(2)).catch(error=>{console.error(error.stack);process.exitCode=4;});
}
