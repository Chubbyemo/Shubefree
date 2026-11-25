// 往 ~/.claude/settings.json 里加 Clawd Buddy 的 hooks（先备份，可重复运行）
// 用法：node setup-hooks.js <clawd-hook.js 的绝对路径>
const fs = require("fs");
const os = require("os");
const path = require("path");
const hookScript = process.argv[2];
const file = path.join(os.homedir(), ".claude", "settings.json");
const EVENTS = ["SessionStart", "UserPromptSubmit", "PreToolUse", "PostToolUseFailure", "Notification",
  "PermissionRequest", "Stop", "SubagentStart", "SubagentStop", "PreCompact", "SessionEnd"];
const WITH_MATCHER = new Set(["PreToolUse", "PostToolUseFailure", "PermissionRequest"]);

let cfg = {};
if (fs.existsSync(file)) {
  cfg = JSON.parse(fs.readFileSync(file, "utf8"));
  fs.copyFileSync(file, file + ".before-clawd");
} else {
  fs.mkdirSync(path.dirname(file), { recursive: true });
}
cfg.hooks = cfg.hooks || {};
for (const ev of EVENTS) {
  const list = (cfg.hooks[ev] || []).filter(
    (e) => !(e.hooks || []).some((h) => String(h.command || "").includes("clawd-hook.js")));
  const entry = { hooks: [{ type: "command", command: `node "${hookScript}" ${ev}`, timeout: 2 }] };
  if (WITH_MATCHER.has(ev)) entry.matcher = "*";
  list.push(entry);
  cfg.hooks[ev] = list;
}
fs.writeFileSync(file, JSON.stringify(cfg, null, 2) + "\n");
console.log("已写入 " + file);
