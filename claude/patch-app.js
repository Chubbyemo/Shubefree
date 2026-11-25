// 把 claude-bridge 接进 Clawd Buddy 的 main.js / preload.js（可重复运行）
// 用法：node patch-app.js <clawd-buddy 目录>
const fs = require("fs");
const path = require("path");
const dir = process.argv[2];
const main = path.join(dir, "src", "main.js");
const preload = path.join(dir, "src", "preload.js");

let s = fs.readFileSync(main, "utf8");
if (!s.includes("claude-bridge")) {
  const anchor = "const STATE_PRIORITY = _state.STATE_PRIORITY;\n";
  if (!s.includes(anchor) || !s.includes("    createWindow();\n")) {
    console.error("main.js 结构变了，没法自动接上 Claude，跳过"); process.exit(1);
  }
  s = s.replace(anchor, anchor + `let _claudeBridge = null;
function startClaudeBridgeOnce() {
  if (_claudeBridge) return;
  _claudeBridge = require("./claude-bridge")({ updateSession, sendToRenderer, log: (m) => sessionLog(m) });
}
`);
  s = s.replace("    createWindow();\n", "    createWindow();\n    startClaudeBridgeOnce();\n");
  fs.writeFileSync(main, s);
}

let p = fs.readFileSync(preload, "utf8");
if (!p.includes("onClaudeEvent")) {
  p = p.replace("  onPlaySound:", '  onClaudeEvent: (cb) => ipcRenderer.on("claude-event", (_, ev) => cb(ev)),\n  onPlaySound:');
  fs.writeFileSync(preload, p);
}
console.log("已接上 Claude 桥");
