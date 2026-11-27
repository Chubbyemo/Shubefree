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

// 小把戏：偷奶酪、横着走、插花（自动随机触发 + 右键菜单）
s = fs.readFileSync(main, "utf8");
if (!s.includes('require("./tricks")')) {
  const a = "let _speechWin = null;\n";
  const b = "    startClaudeBridgeOnce();\n";
  const c = "  teasePet: (source) => teasePet(source),\n";
  if (s.includes(a) && s.includes(b) && s.includes(c)) {
    s = s.replace(a, `let _tricks = null;
function getTricks() {
  if (!_tricks) {
    _tricks = require("./tricks")({
      getState: () => _state.getCurrentState(),
      idleSvg: () => getSvgOverride("idle") || (activeTheme && activeTheme.states.idle[0]),
      isMini: () => _mini.getMiniMode(),
      isDragging: () => dragLocked,
      isHidden: () => petHidden,
      isDnd: () => doNotDisturb,
      getBounds: () => getPetWindowBounds(),
      getWorkArea: (x, y) => getNearestWorkArea(x, y),
      moveTo: (b) => applyPetWindowBounds(b),
      sendToRenderer,
      sendToHitWin,
    });
  }
  return _tricks;
}
` + a);
    s = s.replace(b, b + "    getTricks().start();\n");
    s = s.replace(c, c + "  playHeist: () => getTricks().heist(),\n  playCrab: () => getTricks().crab(),\n  playIkebana: () => getTricks().ikebana(),\n");
    s = s.replace('log: (m) => sessionLog(m) });', 'log: (m) => sessionLog(m), tricks: () => getTricks() });');
    fs.writeFileSync(main, s);
  } else {
    console.error("main.js 结构变了，小把戏没装上");
  }
}
const menu = path.join(dir, "src", "menu.js");
let mn = fs.readFileSync(menu, "utf8");
if (!mn.includes("playHeist")) {
  const anchor = '        click: () => ctx.teasePet("context-menu"),\n      },';
  if (mn.includes(anchor)) {
    mn = mn.replace(anchor, anchor + '\n      { label: "偷块奶酪", click: () => ctx.playHeist && ctx.playHeist() },\n      { label: "横着走", click: () => ctx.playCrab && ctx.playCrab() },\n      { label: "插个花", click: () => ctx.playIkebana && ctx.playIkebana() },');
    fs.writeFileSync(menu, mn);
  }
}

const hitR = path.join(dir, "src", "hit-renderer.js");
let hr = fs.readFileSync(hitR, "utf8");
if (!hr.includes("mix the celebration")) {
  const old = `      firstClickDir = null;
      window.hitAPI.petSingleClick();`;
  const neu = `      const dir = firstClickDir;
      firstClickDir = null;
      // Single click: mix the celebration with the other reactions.
      const pool = [];
      const sideReact = dir === "left" ? leftReact : rightReact;
      if (sideReact) pool.push([sideReact.file, sideReact.duration || 2500], [sideReact.file, sideReact.duration || 2500]);
      if (annoyedReact) pool.push([annoyedReact.file, annoyedReact.duration || 3500]);
      if (doubleReact) for (const f of (doubleReact.files || [doubleReact.file])) pool.push([f, doubleReact.duration || 3500]);
      if (pool.length && Math.random() < 0.75) {
        const [f, d] = pool[Math.floor(Math.random() * pool.length)];
        playReaction(f, d);
      } else {
        window.hitAPI.petSingleClick();
      }`;
  if (hr.includes(old)) { hr = hr.replace(old, neu); fs.writeFileSync(hitR, hr); }
  else console.error("hit-renderer.js 结构变了，单击表情没改上");
}

// 空闲动画按 weight 加权抽（插花出现得多一点）
const tick = path.join(dir, "src", "tick.js");
let tk = fs.readFileSync(tick, "utf8");
if (!tk.includes("a.weight")) {
  const a = "  IDLE_ANIMS = (theme.idleAnimations || []).map(a => ({ svg: a.file, duration: a.duration }));";
  const c = "        const pick = IDLE_ANIMS[Math.floor(Math.random() * IDLE_ANIMS.length)];";
  if (tk.includes(a) && tk.includes(c)) {
    tk = tk.replace(a, "  IDLE_ANIMS = (theme.idleAnimations || []).map(a => ({ svg: a.file, duration: a.duration, weight: a.weight > 0 ? a.weight : 1 }));");
    tk = tk.replace(c, "        let roll = Math.random() * IDLE_ANIMS.reduce((n, a) => n + a.weight, 0);\n        const pick = IDLE_ANIMS.find(a => (roll -= a.weight) < 0) || IDLE_ANIMS[0];");
    fs.writeFileSync(tick, tk);
  } else console.error("tick.js 结构变了，插花权重没改上");
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
