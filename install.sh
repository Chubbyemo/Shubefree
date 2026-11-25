#!/usr/bin/env bash
# 给 Clawd Buddy 装上 Chubby Mouse 主题和说话气泡（Linux / macOS）
# 用法：./install.sh [clawd-buddy 的目录，默认 ./clawd-buddy]
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
TARGET="${1:-$PWD/clawd-buddy}"

if [ ! -d "$TARGET" ]; then
  echo "==> 没找到 $TARGET，先下载 Clawd Buddy"
  git clone https://github.com/bestxiangest/clawd-buddy "$TARGET"
fi
TARGET="$(cd "$TARGET" && pwd)"

if [ -z "${SKIP_NPM:-}" ] && [ ! -x "$TARGET/node_modules/electron/dist/electron" ] \
   && [ ! -d "$TARGET/node_modules/electron/dist/Electron.app" ]; then
  echo "==> 安装依赖（第一次会下载 Electron，需要几分钟）"
  (cd "$TARGET" && npm install)
  # 新版 npm 默认不跑安装脚本，Electron 需要它来下载本体
  (cd "$TARGET" && npm approve-scripts electron koffi >/dev/null 2>&1 && npm rebuild electron koffi) || true
fi

echo "==> 复制小老鼠主题"
rm -rf "$TARGET/themes/chubby-mouse"
cp -r "$HERE/theme/chubby-mouse" "$TARGET/themes/"

echo "==> 装上说话气泡"
cp "$HERE/speech/speech.js" "$HERE/speech/speech.css" "$TARGET/src/"
INDEX="$TARGET/src/index.html"
grep -q 'speech.css' "$INDEX" || \
  sed -i.bak 's|<link rel="stylesheet" href="styles.css">|&\n  <link rel="stylesheet" href="speech.css">|' "$INDEX"
grep -q 'speech.js' "$INDEX" || \
  sed -i.bak 's|<script src="renderer.js"></script>|&\n  <script src="speech.js"></script>|' "$INDEX"
rm -f "$INDEX.bak"

echo "==> 接上 Claude Code（Claude 干活时小老鼠会跟着说话）"
cp "$HERE/claude/claude-bridge.js" "$TARGET/src/"
mkdir -p "$TARGET/hooks" && cp "$HERE/claude/clawd-hook.js" "$TARGET/hooks/"
cp "$HERE"/bubble/* "$TARGET/src/"
cp "$HERE/tricks/tricks.js" "$TARGET/src/"
node "$HERE/claude/patch-app.js" "$TARGET" || true
if [ -z "${SKIP_CLAUDE_HOOKS:-}" ]; then
  node "$HERE/claude/setup-hooks.js" "$TARGET/hooks/clawd-hook.js"
fi

if [ "$(uname)" = "Darwin" ]; then
  PREFS="$HOME/Library/Application Support/clawd-buddy/clawd-prefs.json"
else
  PREFS="${XDG_CONFIG_HOME:-$HOME/.config}/clawd-buddy/clawd-prefs.json"
fi
if [ -f "$PREFS" ]; then
  sed -i.bak 's/"theme": *"[^"]*"/"theme": "chubby-mouse"/' "$PREFS" && rm -f "$PREFS.bak"
  echo "==> 已把主题切到 Chubby Mouse"
else
  echo "==> 第一次启动后，右键小家伙 → Theme → Chubby Mouse"
fi

echo
echo "装好了！启动：cd \"$TARGET\" && npm start"
