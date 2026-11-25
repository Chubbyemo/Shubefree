"use strict";

// Speech bubbles: the pet occasionally says something abstract.
// Purely visual, renderer-only. Listens to the same IPC events as renderer.js.
(function () {
  const LINES = {
    idle: [
      "姑姑嘎嘎",
      "我是奶龙",
      "给我一杯米麻鼠",
      "你在说什么啊，我不知道什么 isaac lab 的在哪里",
      "刚刚不小心把你的 C 盘改名了，没关系吧",
      "嘎？",
      "咕噜咕噜咕噜鼠",
      "我是奶龙，我才是奶龙",
      "鼠鼠我啊，今天也是一只鼠",
      "叽",
      "叽叽叽叽叽（翻译：给钱）",
      "你的代码我看了，鼠看不懂",
      "我刚刚把你的 GPU 拿去煮米线了",
      "什么 reward，鼠只认奶酪",
      "我把你的 checkpoint 藏起来了，猜猜在哪",
      "你的机器人能抓起来一块奶酪吗？不能的话鼠不认",
      "鼠鼠不懂什么叫 sim2sim，鼠只懂 鼠2鼠",
      "我帮你把 ckpt_last 改名成 ckpt_最后真的最后_v2 了",
      "下载文件夹里好多 zip，鼠鼠都咬过了",
      "啊？什么？谁？哪？",
      "摸鱼不叫摸鱼，叫鼠鼠休息",
      "奶龙说它今天不来了，我替它上班",
      "我是鼠，你也是鼠，大家都是鼠",
      "冲冲冲！冲哪？不知道",
      "给我一杯米麻鼠，要三分糖",
      "不小心把你的桌面壁纸换成我了，好看吗",
      "我刚给你的 Linux 装了个 Windows（开玩笑的）",
      "你今天 git push 了吗？鼠帮你 push 了（push 进了回收站）",
      "这个 bug 不是鼠写的，是奶龙写的",
      "鼠鼠想要一个属于自己的终端",
      "我在你的 .bashrc 里留了一句晚安",
      "嘎嘎嘎嘎嘎嘎嘎",
      "姑姑嘎嘎，姑姑嘎嘎嘎",
      "我不是在发呆，我是在加载奶龙",
      "你的 loss 为什么不降？可能是鼠坐在上面了",
    ],
    research: [
      "sim2sim 的 gap 是鼠鼠挖的，抱歉",
      "你的视觉延迟不是 latency，是鼠鼠在摄像头前面路过",
      "抓起来又掉了？那叫 dropout，鼠鼠研究过",
      "鼠鼠提议加一个 estimator，估计鼠鼠有没有在偷奶酪",
      "你的机器人 lift 的时候手在抖，是不是没喝米麻鼠",
      "我把你的模型权重吃了一半，现在参数量减半了",
      "最后一个 checkpoint 不是最后一个，下一个才是，永远是下一个",
      "鼠鼠用 Isaac Lab 训练了一只奶龙，它学会了躺平",
      "reward shaping？鼠鼠只会 cheese shaping",
      "你的 policy 在 sim 里是天才，在 real 里是鼠鼠",
      "鼠鼠刚把你的 domain randomization 调成了 domain 随便化",
      "你的 success rate 我看了，比鼠鼠抓奶酪还低一点点",
      "周报写了吗？鼠鼠可以帮你写：本周无事发生",
      "训练跑了三天，loss 是一条很稳定的直线（横的）",
      "导师来了！快把摸鱼的窗口关掉！",
      "鼠鼠在你的论文里加了一个作者：鼠鼠",
      "你的 GPU 温度好高，鼠鼠在上面煎了个蛋",
      "observation 里多加一维吧，叫 鼠鼠的心情",
      "不是 sim2real 难，是 real 太 real 了",
      "你知道吗，PPO 的 P 是 鼠 的意思",
      "鼠鼠把 num_envs 调成 4096 只老鼠了",
      "你的机械臂抓不起来东西？试试抓鼠鼠",
      "这个 bug 我看了，是物理引擎的问题（甩锅）",
      "paper 截稿还有几天？鼠鼠帮你数：不够",
      "我在你的仿真里放了一块奶酪，机器人一直在追它",
      "相机丢帧了？是鼠鼠眨眼了",
      "你的 baseline 是什么？鼠鼠的 baseline 是一块奶酪",
      "实验做完了吗？做完了就再做一遍，科研就是这样",
    ],
    mischief: [
      "我在你的仿真里把重力调成了 0.5，机器人现在会飞了",
      "你的机器人抓不起来东西，是因为鼠鼠在它手上抹了黄油",
      "我给每个 env 都放了一块奶酪，4096 个机器人在抢",
      "我把你的 random seed 改成了我的生日",
      "reward 里偷偷加了一项：给鼠鼠喂奶酪 +100",
      "我把 batch size 改成了 1，这样每个样本都能被好好爱护",
      "你的 policy 收敛了，收敛到鼠鼠这里了",
      "sim 和 real 之间的那条缝，鼠鼠住进去了",
      "我把摩擦系数调成了 0，机器人在仿真里滑冰呢",
      "我在你的场景里加了一只鼠鼠，机器人不敢动了",
      "我把 epsilon 改成了 1，现在全是探索，没有利用",
      "我把 gamma 改成了 0，机器人现在只活在当下",
      "刚刚帮你把 max_iterations 改成了 ∞，不用谢",
      "我把相机的分辨率调成了 2x2，机器人说世界好简单",
      "你的 tensorboard 曲线被鼠鼠画了一只猫",
      "我给机械臂多加了一个关节，现在它会比耶了",
      "我把 timestep 调大了 100 倍，机器人直接穿墙了",
      "仿真里的桌子被鼠鼠啃掉一条腿，物体一直在滚",
      "我把 action noise 调到了 114514，机器人在跳街舞",
      "我把你的 GPU 借给奶龙打游戏了，训练暂停一下哈",
      "你的 eval 我替你跑过了，结果是：奶酪",
      "我把机器人的手换成了鼠鼠的爪子，它学会了偷吃",
      "我把 decimation 改成了 0.5，现在一个动作执行两遍",
      "reward 曲线一直往上？是鼠鼠在后面推",
      "我把物体的质量改成了 1000kg，机器人决定躺平",
      "我把你的 config 用 yaml 写成了一首诗",
      "我把 observation 里的位置和速度调换了，机器人现在很困惑",
      "我在你的场景里加了一阵风，物体都被吹走了",
      "我把物体的弹性调成了 1，奶酪在仿真里弹个不停",
      "我把 episode_length 改成了 1 步，机器人一出生就结束了",
      "我把你的 terrain 换成了一大块奶酪",
      "我把 PD 增益调成了 0，机械臂现在软成面条了",
      "我给 4096 个机器人都发了一杯米麻鼠",
      "我在 domain randomization 里加了一项：随机变成鼠鼠",
      "我把你的 wandb 项目名改成了 鼠鼠的实验",
      "你的训练卡住了？我在给 GPU 做按摩",
    ],
    night: [
      "这么晚了，我把你的训练偷偷改成了 CPU 跑，省电",
      "凌晨了，我在你的仿真里关了灯，机器人看不见了",
      "你睡吧，我帮你盯着训练（我也睡了）",
      "深夜给 reward 加了一项：早点睡 +1000",
      "我把你的闹钟设成了 loss 降到 0 的时候响",
    ],
    thinking: [
      "我在想把你的 learning rate 再改成多少",
      "让我想想你的 reward 里还能加点什么",
      "思考中：要不要把重力调成负的",
      "我在想你的 config 里哪个参数最好玩",
    ],
    working: [
      "我在帮你调参，现在 learning rate 是 114514",
      "噼里啪啦，正在把你的 num_envs 改成 1",
      "我在你的代码里加了一行 if 鼠鼠: reward += 100",
      "正在把你的仿真改成鼠鼠视角",
    ],
    error: [
      "报错了？不是我改的 learning rate，是另一只鼠",
      "我就改了一点点重力，怎么全炸了",
      "这个报错是我在你代码里藏的彩蛋",
      "糟了，我把 timestep 改成负数了，时间开始倒流",
    ],
    attention: [
      "训练完了！reward 全是鼠鼠给的",
      "成功了！因为我把成功的标准改成了 0",
      "完成！机器人学会了给鼠鼠递奶酪",
    ],
    notification: [
      "快来看！你的机器人在仿真里跳舞了",
      "喂！你的 loss 变成 NaN 了，不是我干的",
      "叮！你的 GPU 想和你谈谈",
    ],
    yawning: ["好困，我把 batch size 调小一点再睡", "哈——顺手把 max_iterations 改成 3"],
    dozing: ["我睡一会儿，训练先暂停一下哈", "zzz……别动我的 learning rate……"],
    sleeping: [
      "zzZ……梦里机器人都在喝醉……",
      "梦见 sim2sim 的 gap 被我填上了……又挖开了",
      "zzZ……reward +114514……",
      "zzZ……learning rate……再大一点……",
      "梦话：我没有动你的 config……真的……",
      "zzZ……4096 个机器人在给我唱摇篮曲……",
      "梦见 Isaac Lab 的派对还没结束……",
      "zzZ……把重力……调成……0……",
      "梦里的 loss 是一条下降的曲线，好美……",
    ],
    waking: ["我醒了！我睡着的时候谁改了我改过的参数", "刚才梦见你的机器人穿墙了，原来是真的", "我醒了，你的训练跑完了吗？没有？那我再改改"],
    sweeping: ["我在清理你的日志，清到只剩一行：一切正常", "把你的 bug 扫到仿真的地板下面了"],
    carrying: ["我在搬你的 checkpoint，搬到奶龙家里", "这个 rollout 好重，我扛走了"],
    juggling: ["我同时开了 4096 个 env，每个都在开派对", "三个实验一起跑，全被我改了 seed"],
    building: ["我在仿真里盖了一堵墙，机器人过不去了", "施工中：正在给机器人装鼠鼠爪子"],
    poke: [
      "你戳我一下，我就把 learning rate 再乘 10",
      "别戳了，我正在改你的 reward",
      "戳一下，你的仿真里就多一个醉酒的机器人",
      "再戳我就把 seed 改成随机的随机",
      "戳我？我刚把你的重力调成了 0.1",
      "你戳的这一下被我记进了 tensorboard",
    ],
    annoyed: [
      "好好好我投降，learning rate 我改回来（改成 114515）",
      "别戳了！我把你的 checkpoint 都还给你还不行吗",
    ],
    drag: [
      "你把我拖走了，可我已经在你的仿真里留了个后门",
      "放我下来！我的 learning rate 还没改完！",
      "你要带我去哪？Isaac Lab 吗？那里有派对",
      "被拖走也没用，sim2sim 的 gap 我已经挖好了",
    ],
    double: [
      "双击！解锁隐藏功能：机器人全部喝醉",
      "你双击我，我就双倍你的 learning rate",
    ],
  };

  // 最爱的几句：平时出现的概率更高
  const FAVORITES = [
    "我刚刚在你的 Isaac Lab 里开了个派对，机器人都喝醉了",
    "sim2sim 的 gap 是鼠鼠挖的，抱歉",
    "我把你的 learning rate 改成 114514 了",
  ];

  // 小把戏：偷奶酪、横着走
  LINES.heist = [
    "嘘……我去去就回",
    "这块奶酪现在归鼠鼠了",
    "我什么都没拿，你看错了",
    "偷奶酪的事，你就当没看见",
  ];
  LINES.crab = [
    "横着走，我是螃蟹鼠",
    "让一让让一让，螃蟹过马路",
    "我在测试新的 locomotion policy，只会横着走",
    "reward 里没写要正着走，所以我横着走",
    "这就是 sim2sim 的 gap 吗，步态全歪了",
  ];

  const BUBBLE_MS = 10000;
  const MIN_GAP_MS = 3500;
  const IDLE_MIN_MS = 15 * 1000;
  const IDLE_MAX_MS = 15 * 1000;
  const STATE_CHANCE = 0.6;

  const bubble = document.createElement("div");
  bubble.id = "speech-bubble";
  document.body.appendChild(bubble);

  let muted = false;
  let mini = false;
  let hideTimer = null;
  let lastSpoke = 0;
  let lastLine = "";
  let currentState = "idle";
  let idleTimer = null;

  function pick(list) {
    if (!list || !list.length) return null;
    let line = list[Math.floor(Math.random() * list.length)];
    if (line === lastLine && list.length > 1) {
      line = list[(list.indexOf(line) + 1) % list.length];
    }
    return line;
  }

  function pickSome(list, n) {
    const out = [];
    for (let i = 0; i < n; i++) out.push(list[Math.floor(Math.random() * list.length)]);
    return out;
  }

  function say(key, force) {
    if (muted || mini) return;
    const now = Date.now();
    if (!force && now - lastSpoke < MIN_GAP_MS) return;
    let list = LINES[key];
    if (key === "idle") {
      // 权重：捣乱实验的台词最多，最爱的三句更多，其它的偶尔出现
      list = []
        .concat(LINES.mischief, LINES.mischief, LINES.mischief, LINES.mischief, LINES.mischief)
        .concat(FAVORITES, FAVORITES, FAVORITES, FAVORITES, FAVORITES, FAVORITES, FAVORITES, FAVORITES)
        .concat(LINES.research)
        .concat(pickSome(LINES.idle, 6));
      const h = new Date().getHours();
      if (h >= 23 || h < 6) list = list.concat(LINES.night, LINES.night, LINES.night);
    }
    if (key === "sleeping") list = list.concat(LINES.dozing);
    if (key === "idle" && claudeBusy()) list = topicLines().concat(topicLines(), list.slice(0, 20));
    const line = pick(list);
    if (!line) return;
    show(line, now);
  }

  function show(line, now) {
    if (muted || mini || !line) return;
    lastLine = line;
    lastSpoke = now || Date.now();
    // 有独立气泡窗口时显示在所有动画之上；没有就退回到宠物窗口里
    if (window.electronAPI && window.electronAPI.showSpeech) {
      window.electronAPI.showSpeech(line, BUBBLE_MS);
      return;
    }
    bubble.textContent = line;
    bubble.classList.add("show");
    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => bubble.classList.remove("show"), BUBBLE_MS);
  }

  function hideNow() {
    clearTimeout(hideTimer);
    bubble.classList.remove("show");
    if (window.electronAPI && window.electronAPI.hideSpeech) window.electronAPI.hideSpeech();
  }

  function scheduleIdle() {
    clearTimeout(idleTimer);
    const delay = IDLE_MIN_MS + Math.random() * (IDLE_MAX_MS - IDLE_MIN_MS);
    idleTimer = setTimeout(() => {
      // 睡着了也说话（说梦话），其它状态都说平时的台词
      if (/sleep|collaps|doz|yawn/.test(currentState)) say("sleeping");
      else say("idle");
      scheduleIdle();
    }, delay);
  }

  function keyForState(state, svg) {
    const s = String(state || "");
    const f = String(svg || "");
    if (/heist/.test(f)) return "heist";
    if (/crab/.test(f)) return "crab";
    if (s === "idle") return null;
    if (LINES[s]) return s;
    if (/build/.test(s + f)) return "building";
    if (/juggl|conduct/.test(s + f)) return "juggling";
    if (/sweep/.test(s + f)) return "sweeping";
    if (/carry/.test(s + f)) return "carrying";
    if (/happy|attention/.test(s + f)) return "attention";
    if (/think/.test(s + f)) return "thinking";
    if (/work|typing/.test(s + f)) return "working";
    if (/sleep/.test(s)) return "sleeping";
    return null;
  }

  const api = window.electronAPI;
  if (!api) return;

  api.onStateChange((state, svg) => {
    const prev = currentState;
    currentState = state;
    if (state === prev && !/heist|crab/.test(String(svg || ""))) return;
    const key = keyForState(state, svg);
    if (!key) return;
    const sure = key === "waking" || key === "error" || key === "notification" || key === "heist" || key === "crab";
    if (sure || Math.random() < STATE_CHANCE) say(key);
  });

  api.onPlayClickReaction((svg) => {
    const f = String(svg || "");
    if (/annoy/.test(f)) say("annoyed", true);
    else if (/double/.test(f)) say("double", true);
    else say("poke");
  });

  api.onStartDragReaction(() => say("drag", true));
  api.onDndChange((enabled) => { muted = !!enabled; if (muted) hideNow(); });
  api.onMiniModeChange((enabled) => { mini = !!enabled; if (mini) hideNow(); });

  // ── 连上 Claude Code：根据 Claude 正在干的事说话 ──
  // 真实的文件名 / 命令只在本机桌宠里显示，不会写进任何文件。
  const TOPICS = [
    { re: /isaac|sim\b|仿真|mujoco|gazebo|sim2sim|sim2real/i, lines: [
      "Claude 在弄仿真，我悄悄把重力调成了 9.9",
      "又是仿真！我在你的场景里藏了一块香蕉皮",
      "sim2sim 的 gap 是鼠鼠挖的，抱歉",
      "我刚刚在你的 Isaac Lab 里开了个派对，机器人都喝醉了",
    ]},
    { re: /reward|奖励|policy|ppo|rl\b|强化/i, lines: [
      "reward 写好了吗？我偷偷加了一项「给鼠鼠喂饭」",
      "policy 学会的第一件事是给我鞠躬",
      "我把你的 reward 乘了个 -1，看看会发生什么",
    ]},
    { re: /train|训练|lr|learning rate|epoch|loss|ckpt|checkpoint/i, lines: [
      "我把你的 learning rate 改成 114514 了",
      "loss 在下降！……是我拿铅笔往下画的",
      "checkpoint 我帮你存了，存在我的奶酪洞里",
    ]},
    { re: /bug|报错|error|fix|修|崩/i, lines: [
      "这个 bug 不是我放的……大概不是",
      "修 bug 的时候我在旁边加 bug，很公平",
    ]},
    { re: /git|commit|push|仓库|repo/i, lines: [
      "commit message 我帮你写好了：鼠鼠到此一游",
      "push 之前让我先往里面塞一根奶酪",
    ]},
    { re: /桌宠|鼠|气泡|speech|clawd/i, lines: [
      "你们在讨论我？我脸红了",
      "Claude 在给我加新台词，我要说一万句",
    ]},
  ];
  const GENERIC_BUSY = [
    "Claude 在干活，鼠鼠在监工",
    "我在旁边帮 Claude 递奶酪",
    "Claude 写一行，我改一行",
  ];
  let lastPrompt = "";
  let lastClaudeAt = 0;
  let lastToolSay = 0;

  function claudeBusy() { return Date.now() - lastClaudeAt < 90 * 1000; }
  function topicLines() {
    const out = [];
    for (const t of TOPICS) if (t.re.test(lastPrompt)) out.push(...t.lines);
    return out.length ? out : GENERIC_BUSY;
  }
  function pickFrom(list) { return list[Math.floor(Math.random() * list.length)]; }
  function fill(list, x) { return pickFrom(list).replace("{x}", x); }

  const TOOL_LINES = {
    edit: ["鼠鼠正在改 {x}，放心，只动了一点点", "{x} 被我加了一行注释：鼠鼠到此一游", "正在改 {x}……顺便把缩进换成了奶酪"],
    write: ["新建了 {x}，里面藏了一只鼠", "{x} 写好了，作者栏写的是鼠鼠"],
    read: ["Claude 在看 {x}，我也在看，看不懂", "正在偷看 {x}"],
    bash: ["在跑 {x}，我赌它会炸", "{x}……这个命令是我教 Claude 的", "跑 {x} 之前我先按了一下回车"],
    search: ["在找 {x}，我知道在哪但我不说", "搜 {x} 呢，鼠鼠帮忙翻垃圾桶"],
    web: ["Claude 去 {x} 冲浪了，带我一个", "在逛 {x}"],
    agent: ["Claude 叫了个小弟：{x}", "派了个分身去 {x}，鼠鼠也要分身"],
    other: ["Claude 在用 {x}，鼠鼠在用爪子"],
  };
  function toolKind(tool) {
    if (/Edit|MultiEdit|NotebookEdit/.test(tool)) return "edit";
    if (/Write/.test(tool)) return "write";
    if (/Read/.test(tool)) return "read";
    if (/Bash/.test(tool)) return "bash";
    if (/Grep|Glob|Search/.test(tool)) return "search";
    if (/Web|Fetch/.test(tool)) return "web";
    if (/Agent|Task/.test(tool)) return "agent";
    return "other";
  }
  function short(x, n) { x = String(x || ""); return x.length > n ? x.slice(0, n - 1) + "…" : x; }

  if (api.onClaudeEvent) api.onClaudeEvent((ev) => {
    if (!ev) return;
    lastClaudeAt = Date.now();
    const now = Date.now();
    switch (ev.event) {
      case "UserPromptSubmit":
        if (ev.prompt) lastPrompt = ev.prompt;
        show(pickFrom(topicLines().concat([
          "收到！让鼠鼠想想……顺便把你的 seed 改了",
          "你说的我都听到了，我决定假装没听到",
        ])));
        break;
      case "PreToolUse": {
        // 工具调用很密，最多 6 秒说一次
        if (now - lastToolSay < 6000) return;
        lastToolSay = now;
        const kind = toolKind(ev.tool || "");
        const x = short(ev.target || ev.tool, kind === "bash" ? 28 : 36) || ev.tool;
        show(fill(TOOL_LINES[kind], x));
        break;
      }
      case "PostToolUseFailure":
        show(pickFrom(["不是我干的！……好吧是我", "炸了！我就说会炸", "报错了，鼠鼠先溜了"]));
        break;
      case "PermissionRequest":
      case "Notification":
        show(pickFrom(["快来！Claude 要你点一下", "Claude 在等你，我在等奶酪", "喂喂，有人找你"]));
        break;
      case "Stop":
        show(pickFrom(["搞定了，你检查一下有没有被我加料", "Claude 干完了，功劳分我一半", "做完了！现在可以给我一杯米麻鼠了吗"]));
        break;
      case "PreCompact":
        show(pickFrom(["Claude 在整理记忆，我在帮它忘掉一些事"]));
        break;
      case "SubagentStart":
        show(pickFrom(["Claude 叫了个帮手，鼠鼠也想要帮手"]));
        break;
      default:
        break;
    }
  });

  scheduleIdle();
  setTimeout(() => say("idle"), 2500);
})();
