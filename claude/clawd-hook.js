#!/usr/bin/env node
// Claude Code hook → Clawd Buddy. Usage in settings.json:
//   node /path/to/clawd-hook.js <EventName>
// Reads the hook JSON from stdin, keeps a few short fields, POSTs them to
// the pet on 127.0.0.1. Never blocks Claude: always exits 0 within ~1s.
const http = require("http");
const path = require("path");

const event = process.argv[2] || "";
const PORT = Number(process.env.CLAWD_BRIDGE_PORT) || 23333;
const done = () => process.exit(0);
setTimeout(done, 1000).unref();

let raw = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (c) => { raw += c; });
process.stdin.on("end", () => {
  let d = {};
  try { d = JSON.parse(raw || "{}"); } catch {}
  const input = d.tool_input || {};
  let target = "";
  if (input.file_path || input.notebook_path) target = path.basename(input.file_path || input.notebook_path);
  else if (typeof input.command === "string") target = input.command.split("\n")[0];
  else if (input.pattern) target = String(input.pattern);
  else if (input.url) { try { target = new URL(input.url).hostname; } catch {} }
  else if (input.description) target = String(input.description);

  const payload = JSON.stringify({
    event: d.hook_event_name || event,
    session_id: d.session_id || "",
    cwd: d.cwd || "",
    tool: d.tool_name || "",
    target: target.slice(0, 120),
    prompt: typeof d.prompt === "string" ? d.prompt.slice(0, 400) : "",
    message: typeof d.message === "string" ? d.message.slice(0, 120) : "",
  });
  const req = http.request({
    host: "127.0.0.1", port: PORT, path: "/event", method: "POST",
    headers: { "Content-Type": "application/json", "Content-Length": Buffer.byteLength(payload) },
    timeout: 800,
  }, (res) => { res.resume(); res.on("end", done); });
  req.on("error", done);
  req.on("timeout", () => { req.destroy(); done(); });
  req.end(payload);
});
