// claude-bridge.js — receives Claude Code hook events on 127.0.0.1 and
// drives the pet: state changes via updateSession, live lines via IPC.
const http = require("http");

const PORT = Number(process.env.CLAWD_BRIDGE_PORT) || 23333;

const EVENT_STATE = {
  SessionStart: "idle",
  UserPromptSubmit: "thinking",
  PreToolUse: "working",
  PostToolUse: "working",
  PostToolUseFailure: "error",
  SubagentStart: "juggling",
  SubagentStop: "working",
  Stop: "attention",
  Notification: "notification",
  PermissionRequest: "notification",
  PreCompact: "sweeping",
  SessionEnd: "sleeping",
};

function clip(s, n) {
  if (typeof s !== "string") return "";
  s = s.replace(/\s+/g, " ").trim();
  return s.length > n ? s.slice(0, n - 1) + "…" : s;
}

module.exports = function startClaudeBridge({ updateSession, sendToRenderer, log, tricks }) {
  const server = http.createServer((req, res) => {
    // 本机手动触发小把戏：curl -X POST 127.0.0.1:23333/trick/heist 或 /trick/crab
    const m = req.method === "POST" && /^\/trick\/(heist|crab)$/.exec(req.url || "");
    if (m) {
      const t = tricks && tricks();
      const ok = t && t[m[1]]();
      res.writeHead(ok ? 204 : 409); res.end(ok ? "" : (t ? t.why() : "")); return;
    }
    if (req.method !== "POST" || req.url !== "/event") {
      res.writeHead(404); res.end(); return;
    }
    let body = "";
    req.on("data", (c) => { body += c; if (body.length > 64 * 1024) req.destroy(); });
    req.on("end", () => {
      res.writeHead(204); res.end();
      let msg;
      try { msg = JSON.parse(body); } catch { return; }
      const event = msg.event;
      const state = EVENT_STATE[event];
      if (!state) return;
      const sid = clip(msg.session_id, 80) || "claude";
      try {
        updateSession(sid, state, event, { cwd: msg.cwd || null, agentId: "claude-code" });
      } catch (e) { log && log(`bridge updateSession failed: ${e.message}`); }
      sendToRenderer("claude-event", {
        event,
        tool: clip(msg.tool, 40),
        target: clip(msg.target, 60),
        prompt: clip(msg.prompt, 300),
        message: clip(msg.message, 80),
      });
    });
  });
  server.on("error", (e) => log && log(`bridge listen failed: ${e.message}`));
  server.listen(PORT, "127.0.0.1");
  return server;
};
