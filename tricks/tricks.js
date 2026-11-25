// tricks.js — little shows the mouse puts on by itself: cheese heist, crab-walking
// sideways across the screen. Plays only while the pet is idle and nothing is going on.
const HEIST_SVG = "mouse-trick-heist.svg";
const HEIST_MS = 13300;
const CRAB_SVG = "mouse-trick-crab.svg";
const CRAB_SPEED = 160;        // DIP per second, a brisk sideways scuttle
const MIN_GAP_MS = 3 * 60 * 1000;
const MAX_GAP_MS = 7 * 60 * 1000;

module.exports = function createTricks(ctx) {
  let busy = false;
  let timer = null;
  let started = false;

  function canPlay() {
    return !busy && ctx.getState() === "idle" && !ctx.isMini() && !ctx.isDragging()
      && !ctx.isHidden() && !ctx.isDnd();
  }

  function show(svg) {
    ctx.sendToRenderer("state-change", "idle", svg);
    ctx.sendToHitWin("hit-state-sync", { currentSvg: svg });
  }

  function finish() {
    busy = false;
    if (ctx.getState() === "idle") show(ctx.idleSvg());
    schedule();
  }

  function heist() {
    if (!canPlay()) return false;
    busy = true;
    show(HEIST_SVG);
    setTimeout(finish, HEIST_MS);
    return true;
  }

  function crab() {
    if (!canPlay()) return false;
    const b = ctx.getBounds();
    if (!b) return false;
    const wa = ctx.getWorkArea(b.x + b.width / 2, b.y + b.height / 2);
    if (!wa) return false;
    const dir = b.x + b.width / 2 < wa.x + wa.width / 2 ? 1 : -1;
    const targetX = dir > 0 ? wa.x + wa.width - b.width : wa.x;
    busy = true;
    show(CRAB_SVG);
    const startX = b.x;
    const dist = Math.abs(targetX - startX);
    const total = Math.max(500, (dist / CRAB_SPEED) * 1000);
    const t0 = Date.now();
    const iv = setInterval(() => {
      // 被拖走、来活了、进 mini 就停下
      if (ctx.isDragging() || ctx.isMini() || ctx.getState() !== "idle") {
        clearInterval(iv); finish(); return;
      }
      const k = Math.min(1, (Date.now() - t0) / total);
      const cur = ctx.getBounds();
      ctx.moveTo({ ...cur, x: Math.round(startX + (targetX - startX) * k) });
      if (k >= 1) { clearInterval(iv); finish(); }
    }, 16);
    return true;
  }

  function schedule() {
    clearTimeout(timer);
    if (!started) return;
    const delay = MIN_GAP_MS + Math.random() * (MAX_GAP_MS - MIN_GAP_MS);
    timer = setTimeout(() => {
      if (!canPlay()) { schedule(); return; }
      (Math.random() < 0.5 ? heist : crab)();
      if (!busy) schedule();
    }, delay);
  }

  function why() {
    return JSON.stringify({ busy, state: ctx.getState(), mini: ctx.isMini(), drag: ctx.isDragging(),
      hidden: ctx.isHidden(), dnd: ctx.isDnd() });
  }

  return {
    why,
    start() { started = true; schedule(); },
    heist,
    crab,
  };
};
