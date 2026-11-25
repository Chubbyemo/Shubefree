// speech-window-main.js — a separate transparent window that floats above the
// pet window, so speech bubbles never cover any animation.
const { BrowserWindow } = require("electron");
const path = require("path");

module.exports = function createSpeechWindow({ getPetBounds, getWorkArea, isLinux, linuxType, isHidden }) {
  let bw = null;
  let hideTimer = null;
  let visible = false;
  const W_MIN = 240;
  const H = 120;

  function size() {
    const pet = getPetBounds();
    const w = Math.max(W_MIN, Math.round(pet ? pet.width * 1.5 : W_MIN));
    return { w, h: H };
  }

  function ensure() {
    if (bw && !bw.isDestroyed()) return bw;
    const { w, h } = size();
    bw = new BrowserWindow({
      width: w, height: h, x: -10000, y: -10000,
      frame: false, transparent: true, alwaysOnTop: true, resizable: false,
      skipTaskbar: true, hasShadow: false, fullscreenable: false,
      ...(isLinux ? { type: linuxType } : {}),
      webPreferences: { backgroundThrottling: false },
    });
    // 窗口一直开着（透明、鼠标穿透），只切换气泡内容；
    // 反复隐藏/显示在 Linux 上会丢掉置顶
    bw.setFocusable(false);
    bw.setIgnoreMouseEvents(true);
    bw.showInactive();
    bw.loadFile(path.join(__dirname, "speech-window.html"));
    bw.webContents.once("did-finish-load", () => {
      setTimeout(() => {
        if (!bw || bw.isDestroyed()) return;
        bw.setAlwaysOnTop(false);
        bw.setAlwaysOnTop(true, "screen-saver");
      }, 500);
    });
    return bw;
  }

  function reposition() {
    if (!bw || bw.isDestroyed()) return;
    const pet = getPetBounds();
    if (!pet) return;
    const { w, h } = size();
    let x = Math.round(pet.x + pet.width / 2 - w / 2);
    let y = Math.round(pet.y - h + 6);
    const wa = getWorkArea(pet.x + pet.width / 2, pet.y + pet.height / 2);
    if (wa) {
      x = Math.min(Math.max(x, wa.x), wa.x + wa.width - w);
      if (y < wa.y) y = wa.y;
    }
    bw.setBounds({ x, y, width: w, height: h });
  }

  function run(js) {
    const b = ensure();
    const go = () => b.webContents.executeJavaScript(js).catch(() => {});
    if (b.webContents.isLoading()) b.webContents.once("did-finish-load", go);
    else go();
  }

  function show(text, ms) {
    if (isHidden && isHidden()) return;
    ensure();
    reposition();
    run(`window.setSpeech(${JSON.stringify(String(text))})`);
    visible = true;
    clearTimeout(hideTimer);
    hideTimer = setTimeout(hide, Math.max(1000, Number(ms) || 10000));
  }

  function hide() {
    clearTimeout(hideTimer);
    if (!bw || bw.isDestroyed() || !visible) return;
    visible = false;
    run("window.clearSpeech()");
  }

  return { show, hide, reposition };
};
