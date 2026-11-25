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
    ],
    night: [
      "这么晚了还不睡，鼠鼠要告诉奶龙了",
      "深夜的米麻鼠特别香",
      "我刚刚在你的 Isaac Lab 里开了个派对，机器人都喝醉了",
      "睡吧，训练会自己跑完的（大概）",
      "凌晨了，你的 GPU 说它想回家",
    ],
    thinking: [
      "鼠鼠在思考……思考失败",
      "让我想想……嘎？",
      "我的脑子只有一块奶酪那么大",
      "这个问题太难了，问奶龙吧",
    ],
    working: [
      "鼠鼠在敲代码！敲的是 asdfghjkl",
      "我在帮你训练模型，用爪子",
      "噼里啪啦，鼠也不知道在写啥",
      "我把你的 learning rate 改成 114514 了",
    ],
    error: [
      "坏了坏了坏了坏了",
      "不是鼠干的！是奶龙！",
      "完蛋，鼠鼠把东西弄坏了，你先别看",
      "呜呜呜鼠鼠要被删掉了吗",
    ],
    attention: [
      "姑姑嘎嘎！做完啦！",
      "耶！奖励鼠鼠一杯米麻鼠！",
      "成功了！虽然鼠不知道什么成功了",
    ],
    notification: [
      "喂喂喂！看鼠！",
      "有人找你！是奶龙吗？",
      "叽！叽！叽！",
    ],
    yawning: ["哈——鼠——", "鼠鼠的电量只剩 1% 了"],
    dozing: ["鼠鼠没睡……鼠鼠在闭眼 debug……", "姑……姑……嘎……"],
    sleeping: ["zzZ……米麻鼠……", "梦里我是奶龙", "zzZ……不要关我的进程……"],
    waking: ["啊？鼠鼠睡着了？", "我刚梦见你的 C 盘了", "谁！谁偷了我的米麻鼠！"],
    sweeping: ["鼠鼠帮你清理缓存！清掉了 200G", "扫扫扫，把 bug 扫到奶龙那边"],
    carrying: ["这个文件好重，是 ckpt 吗", "鼠鼠在搬家，搬到你的 home 目录"],
    juggling: ["三个任务一起跑！鼠鼠要冒烟了", "多线程？鼠鼠只有一个脑子"],
    building: ["鼠鼠在盖房子，用你的显存", "施工中！请奶龙绕行"],
    poke: [
      "嘎！",
      "别戳鼠鼠！鼠鼠会咬人的（不会）",
      "你再戳我就去改你的 C 盘",
      "戳一下，一杯米麻鼠",
      "姑姑嘎嘎？",
      "我是奶龙！别戳奶龙！",
    ],
    annoyed: ["好了好了鼠鼠投降", "再戳鼠鼠就去告诉奶龙"],
    drag: [
      "啊啊啊啊鼠鼠飞起来了",
      "放鼠下来！鼠要去喝米麻鼠！",
      "你要带鼠鼠去哪？Isaac Lab 吗？",
      "嘎嘎嘎嘎嘎嘎",
    ],
    double: ["鼠鼠跳舞！姑姑嘎嘎！", "鼠鼠升天了，天上有米麻鼠吗"],
  };

  // 最爱的几句：平时出现的概率更高
  const FAVORITES = [
    "我刚刚在你的 Isaac Lab 里开了个派对，机器人都喝醉了",
    "sim2sim 的 gap 是鼠鼠挖的，抱歉",
    "我把你的 learning rate 改成 114514 了",
  ];

  const BUBBLE_MS = 4200;
  const MIN_GAP_MS = 3500;
  const IDLE_MIN_MS = 70 * 1000;
  const IDLE_MAX_MS = 180 * 1000;
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

  function say(key, force) {
    if (muted || mini) return;
    const now = Date.now();
    if (!force && now - lastSpoke < MIN_GAP_MS) return;
    let list = LINES[key];
    if (key === "idle") {
      list = list.concat(LINES.research, LINES.mischief, FAVORITES, FAVORITES, FAVORITES);
      const h = new Date().getHours();
      if (h >= 23 || h < 6) list = list.concat(LINES.night, LINES.night);
    }
    const line = pick(list);
    if (!line) return;
    lastLine = line;
    lastSpoke = now;
    bubble.textContent = line;
    bubble.classList.add("show");
    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => bubble.classList.remove("show"), BUBBLE_MS);
  }

  function hideNow() {
    clearTimeout(hideTimer);
    bubble.classList.remove("show");
  }

  function scheduleIdle() {
    clearTimeout(idleTimer);
    const delay = IDLE_MIN_MS + Math.random() * (IDLE_MAX_MS - IDLE_MIN_MS);
    idleTimer = setTimeout(() => {
      if (currentState === "idle") say("idle");
      scheduleIdle();
    }, delay);
  }

  function keyForState(state, svg) {
    const s = String(state || "");
    const f = String(svg || "");
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
    if (state === prev) return;
    const key = keyForState(state, svg);
    if (!key) return;
    const sure = key === "waking" || key === "error" || key === "notification";
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

  scheduleIdle();
  setTimeout(() => say("idle"), 2500);
})();
