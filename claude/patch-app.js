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

// 独立气泡窗口：气泡浮在所有动画上面
s = fs.readFileSync(main, "utf8");
if (!s.includes("speech-window-main")) {
  const a = "let _claudeBridge = null;\n";
  const b = "      repositionFloatingBubbles();\n    };";
  const c = '  ipcMain.on("pause-cursor-polling", () => { idlePaused = true; });\n';
  if (s.includes(a) && s.includes(b) && s.includes(c)) {
    s = s.replace(a, a + `let _speechWin = null;
function getSpeechWin() {
  if (!_speechWin) {
    _speechWin = require("./speech-window-main")({
      getPetBounds: () => getPetWindowBounds(),
      getWorkArea: (x, y) => getNearestWorkArea(x, y),
      isLinux, linuxType: LINUX_WINDOW_TYPE,
      isHidden: () => petHidden || !win || win.isDestroyed() || !win.isVisible(),
    });
  }
  return _speechWin;
}
`);
    s = s.replace(b, "      repositionFloatingBubbles();\n      if (_speechWin) _speechWin.reposition();\n    };");
    s = s.replace(c, c + '  ipcMain.on("speech-show", (_, text, ms) => getSpeechWin().show(text, ms));\n  ipcMain.on("speech-hide", () => { if (_speechWin) _speechWin.hide(); });\n');
    fs.writeFileSync(main, s);
  } else {
    console.error("main.js 结构变了，气泡会留在宠物窗口里");
  }
}

let p = fs.readFileSync(preload, "utf8");
if (!p.includes("showSpeech")) {
  p = p.replace("  onPlaySound:", '  showSpeech: (text, ms) => ipcRenderer.send("speech-show", text, ms),\n  hideSpeech: () => ipcRenderer.send("speech-hide"),\n  onPlaySound:');
}
if (!p.includes("onClaudeEvent")) {
  p = p.replace("  onPlaySound:", '  onClaudeEvent: (cb) => ipcRenderer.on("claude-event", (_, ev) => cb(ev)),\n  onPlaySound:');
}
fs.writeFileSync(preload, p);
console.log("已接上 Claude 桥和气泡窗口");
