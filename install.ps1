# 给 Clawd Buddy 装上 Chubby Mouse 主题和说话气泡（Windows）
# 用法：在 PowerShell 里运行  .\install.ps1 [clawd-buddy 的目录]
param([string]$Target = (Join-Path (Get-Location) "clawd-buddy"))
$ErrorActionPreference = "Stop"
$Here = $PSScriptRoot

if (-not (Test-Path $Target)) {
  Write-Host "==> 没找到 $Target，先下载 Clawd Buddy"
  git clone https://github.com/bestxiangest/clawd-buddy $Target
}
$Target = (Resolve-Path $Target).Path

if (-not (Test-Path (Join-Path $Target "node_modules\electron\dist\electron.exe"))) {
  Write-Host "==> 安装依赖（第一次会下载 Electron，需要几分钟）"
  Push-Location $Target
  npm install
  try { npm approve-scripts electron koffi *> $null; npm rebuild electron koffi } catch {}
  Pop-Location
}

Write-Host "==> 复制小老鼠主题"
$ThemeDst = Join-Path $Target "themes\chubby-mouse"
if (Test-Path $ThemeDst) { Remove-Item -Recurse -Force $ThemeDst }
Copy-Item -Recurse (Join-Path $Here "theme\chubby-mouse") (Join-Path $Target "themes")

Write-Host "==> 装上说话气泡"
Copy-Item (Join-Path $Here "speech\speech.js"), (Join-Path $Here "speech\speech.css") (Join-Path $Target "src")
$Index = Join-Path $Target "src\index.html"
$html = Get-Content -Raw -Encoding UTF8 $Index
if ($html -notmatch "speech.css") {
  $html = $html.Replace('<link rel="stylesheet" href="styles.css">', "<link rel=`"stylesheet`" href=`"styles.css`">`n  <link rel=`"stylesheet`" href=`"speech.css`">")
}
if ($html -notmatch "speech.js") {
  $html = $html.Replace('<script src="renderer.js"></script>', "<script src=`"renderer.js`"></script>`n  <script src=`"speech.js`"></script>")
}
[IO.File]::WriteAllText($Index, $html, (New-Object Text.UTF8Encoding $false))

Write-Host "==> 接上 Claude Code（Claude 干活时小老鼠会跟着说话）"
Copy-Item (Join-Path $Here "claude\claude-bridge.js") (Join-Path $Target "src")
$HookDir = Join-Path $Target "hooks"
New-Item -ItemType Directory -Force $HookDir | Out-Null
Copy-Item (Join-Path $Here "claude\clawd-hook.js") $HookDir
node (Join-Path $Here "claude\patch-app.js") $Target
if (-not $env:SKIP_CLAUDE_HOOKS) {
  node (Join-Path $Here "claude\setup-hooks.js") ((Join-Path $HookDir "clawd-hook.js") -replace '\\','/')
}

$Prefs = Join-Path $env:APPDATA "clawd-buddy\clawd-prefs.json"
if (Test-Path $Prefs) {
  $p = Get-Content -Raw -Encoding UTF8 $Prefs
  $p = $p -replace '"theme":\s*"[^"]*"', '"theme": "chubby-mouse"'
  [IO.File]::WriteAllText($Prefs, $p, (New-Object Text.UTF8Encoding $false))
  Write-Host "==> 已把主题切到 Chubby Mouse"
} else {
  Write-Host "==> 第一次启动后，右键小家伙 -> Theme -> Chubby Mouse"
}

Write-Host ""
Write-Host "装好了！启动：cd `"$Target`"; npm start"
