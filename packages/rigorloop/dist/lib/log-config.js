import { homedir } from "node:os";
import { isAbsolute, join, resolve, win32 } from "node:path";

export const FILE_LOG_LEVELS = Object.freeze(["debug", "info", "warning", "error"]);
export const CONSOLE_LOG_LEVELS = Object.freeze([...FILE_LOG_LEVELS, "off"]);

function invalidLevel(kind) {
  return Object.assign(new Error(`Invalid ${kind} log level.`), { code: "RL_INVALID_LOG_LEVEL" });
}

export function defaultLogDirectory(options = {}) {
  const platform = options.platform ?? process.platform;
  const env = options.env ?? process.env;
  const home = options.home ?? homedir();
  if (platform === "win32") return win32.join(env.LOCALAPPDATA || win32.join(home, "AppData", "Local"), "RigorLoop", "Logs");
  if (platform === "darwin") return join(home, "Library", "Logs", "RigorLoop");
  return join(env.XDG_STATE_HOME || join(home, ".local", "state"), "rigorloop", "logs");
}

export function resolveLogConfig(args = [], options = {}) {
  const env = options.env ?? process.env;
  let fileLevel = env.RIGORLOOP_FILE_LOG_LEVEL || "info";
  let consoleLevel = env.RIGORLOOP_CONSOLE_LOG_LEVEL || "error";
  let fileEnabled = env.RIGORLOOP_FILE_LOG !== "off";
  if (env.RIGORLOOP_FILE_LOG && !["on", "off"].includes(env.RIGORLOOP_FILE_LOG)) throw invalidLevel("file enablement");
  const remaining = [];
  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    if (arg === "--no-file-log") fileEnabled = false;
    else if (arg === "--file-log-level" || arg === "--console-log-level") {
      const value = args[++index];
      if (!value) throw invalidLevel(arg === "--file-log-level" ? "file" : "console");
      if (arg === "--file-log-level") fileLevel = value;
      else consoleLevel = value;
    } else remaining.push(arg);
  }
  if (!FILE_LOG_LEVELS.includes(fileLevel)) throw invalidLevel("file");
  if (!CONSOLE_LOG_LEVELS.includes(consoleLevel)) throw invalidLevel("console");
  const rawDirectory = env.RIGORLOOP_LOG_DIR || defaultLogDirectory(options);
  const windowsAbsolute = (options.platform ?? process.platform) === "win32" && win32.isAbsolute(rawDirectory);
  if (env.RIGORLOOP_LOG_DIR && !isAbsolute(rawDirectory) && !windowsAbsolute) throw Object.assign(new Error("Log directory override must be absolute."), { code: "RL_LOG_UNSAFE_PATH" });
  return { fileLevel, consoleLevel, fileEnabled, directory: windowsAbsolute ? win32.normalize(rawDirectory) : resolve(rawDirectory), args: remaining };
}
