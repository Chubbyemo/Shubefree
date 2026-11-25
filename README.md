# Shubefree 🐭

鼠鼠自由！这是给桌宠 [Clawd Buddy](https://github.com/bestxiangest/clawd-buddy) 做的小老鼠扩展包：

- **Chubby Mouse 像素主题**：Chubbyemo 的小灰鼠像素版，27 段动画，每个动作都参照一幅原画
- **说话气泡**：小老鼠会时不时冒一句沙雕话，被戳、被拖、睡醒的时候也会说

> 「姑姑嘎嘎」「我是奶龙」「给我一杯米麻鼠」
> 「你在说什么啊，我不知道什么 isaac lab 的在哪里」
> 「刚刚不小心把你的 C 盘改名了，没关系吧」
> 「sim2sim 的 gap 是鼠鼠挖的，抱歉」

（都是台词，它不会真的动你的文件。）

## 安装

需要 [Node.js](https://nodejs.org) 和 Git。

**Linux / macOS**

```bash
git clone https://github.com/Chubbyemo/Shubefree
./Shubefree/install.sh
cd clawd-buddy && npm start
```

**Windows（PowerShell）**

```powershell
git clone https://github.com/Chubbyemo/Shubefree
powershell -ExecutionPolicy Bypass -File .\Shubefree\install.ps1
cd clawd-buddy; npm start
```

脚本会在当前目录下载 Clawd Buddy（已经有的话可以把它的路径作为参数传进去），装好依赖，再把主题和说话气泡放进去。重复运行也没关系。

第一次启动如果还是螃蟹，右键它 → Theme → Chubby Mouse。

## 改台词

台词都在 [`speech/speech.js`](speech/speech.js) 开头的 `LINES` 里，按场合分组：

| 分组 | 什么时候说 |
| --- | --- |
| `idle` + `research` + `mischief` | 平时，每 1–3 分钟随机一句 |
| `FAVORITES` | 最爱的几句，平时出现的概率是别的 3 倍 |
| `night` | 晚上 11 点到早上 6 点额外混进来 |
| `poke` / `annoyed` / `double` | 被戳、戳烦了、双击 |
| `drag` | 被拖起来 |
| `waking` / `sleeping` / `dozing` / `yawning` | 睡觉相关 |
| `thinking` / `working` / `error` / `attention` / `notification` 等 | 配合 Claude Code 等工具工作时 |

改完重新运行一次安装脚本，再重启桌宠就生效。勿扰模式和 Mini 模式下不说话。

## 目录

```
theme/chubby-mouse/   像素主题（theme.json + SVG 动画）
speech/speech.js      说话气泡逻辑和台词
speech/speech.css     气泡样式
install.sh            Linux / macOS 安装脚本
install.ps1           Windows 安装脚本
```

## 版权

小老鼠形象和主题美术 © Chubbyemo。Clawd Buddy 本体及其自带美术归原作者所有，本仓库不包含它们。
