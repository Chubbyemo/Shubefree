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

## 小把戏

小老鼠闲着的时候，每隔 3～7 分钟会随机表演一个：

- **偷奶酪**：脚下开个洞钻下去，从旁边的洞探头，踮脚走过去叼走奶酪，飞快跑回洞里，最后抱着奶酪从原地冒出来。
- **横着走**：像螃蟹一样举着小爪子、迈着大脚，从屏幕一边横着走到另一边（在左半边就往右走，反之往左）。

想马上看：右键小老鼠 → 「偷块奶酪」或「横着走」。睡着、Mini 模式、勿扰模式、正在拖动的时候不会表演。

动画是用 [`tools/make_tricks.py`](tools/make_tricks.py) 从原有的帧拼出来的，改完重新生成：

```bash
python3 tools/make_tricks.py theme/chubby-mouse/assets
```

睡觉的时候小老鼠戴着蓝色小睡帽、盖着奶酪被子，是 [`tools/make_sleep.py`](tools/make_sleep.py) 加上去的（重复运行不会叠两层）：

```bash
python3 tools/make_sleep.py theme/chubby-mouse/assets
```

## 连上 Claude Code

装好后，小老鼠会跟着 Claude Code 的动作说话：

| Claude 在干什么 | 小老鼠 |
|---|---|
| 你发了一条消息 | 进入思考状态，按消息里的关键词（仿真、reward、训练、bug、git……）说捣乱台词 |
| 读 / 改 / 新建文件 | "鼠鼠正在改 xxx.py，放心，只动了一点点" |
| 跑命令 | "在跑 python …，我赌它会炸" |
| 报错 | "不是我干的！……好吧是我" |
| 等你批准权限 | "快来！Claude 要你点一下" |
| 干完了 | "搞定了，你检查一下有没有被我加料" |

Claude 干活期间，平时那句每 15 秒一句的台词也会换成和当前话题相关的。

原理：安装脚本在 `~/.claude/settings.json` 里加了几个 hook（原文件会备份成 `settings.json.before-clawd`）。每次事件触发，hook 把工具名、文件名、消息开头这几个字段发到本机 `127.0.0.1:23333`，桌宠收到后切换动画、说话。数据不出本机，桌宠没开时 hook 会直接跳过，不影响 Claude。

不想要的话：装的时候设置 `SKIP_CLAUDE_HOOKS=1`；已经装了的，删掉 `settings.json` 里命令含 `clawd-hook.js` 的那几项。

## 改台词

台词都在 [`speech/speech.js`](speech/speech.js) 开头的 `LINES` 里，按场合分组：

| 分组 | 什么时候说 |
| --- | --- |
| `idle` + `research` + `mischief` | 平时，每 15 秒随机一句，每句停留 10 秒 |
| `FAVORITES` | 最爱的几句，平时出现的概率是别的 3 倍 |
| `night` | 晚上 11 点到早上 6 点额外混进来 |
| `poke` / `annoyed` / `double` | 被戳、戳烦了、双击 |
| `drag` | 被拖起来 |
| `waking` / `sleeping` / `dozing` / `yawning` | 睡觉相关 |
| `thinking` / `working` / `error` / `attention` / `notification` 等 | 配合 Claude Code 等工具工作时 |
| `TOPICS` / `TOOL_LINES`（文件后半段） | 连上 Claude Code 后，按话题和工具说的台词，`{x}` 会换成文件名或命令 |

改完重新运行一次安装脚本，再重启桌宠就生效。勿扰模式和 Mini 模式下不说话。

## 目录

```
theme/chubby-mouse/   像素主题（theme.json + SVG 动画）
speech/speech.js      说话气泡逻辑和台词
speech/speech.css     气泡样式
bubble/               独立的气泡窗口，浮在小老鼠头顶，不挡任何动画
tricks/tricks.js      小把戏的调度（偷奶酪、横着走）
tools/                生成小把戏动画的脚本
claude/               连 Claude Code 用的桥、hook 脚本和配置脚本
install.sh            Linux / macOS 安装脚本
install.ps1           Windows 安装脚本
```

## 版权

小老鼠形象和主题美术 © Chubbyemo。Clawd Buddy 本体及其自带美术归原作者所有，本仓库不包含它们。
