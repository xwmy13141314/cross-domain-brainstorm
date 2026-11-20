# 跨域脑暴 v0.4.0

A cross-domain ideation skill with two modes: **Inspiration** (category collision — ideas first, feasibility later) and **Decision** (transfer causal mechanisms into landable decision cards with owners, budgets, and kill conditions).

一个用于产品/功能/交互/服务/运营流程创新的跨域脑暴 skill，双模式：

- **灵感模式**（创意题默认）：品类碰撞房 → 挑号 → 筛选房。先把品类距离拉满、强行嫁接、看爽点，可行性后置。
- **决策模式**（落地题）：从结构异质领域借“因果机制”，严格映射，产出带预算/执行人/kill 条件的落地卡。

> **模式判定 →（灵感：碰撞房 → 挑号 → 筛选房 ｜ 决策：问题解码 → 距离采样 → 机制卡 → 结构嫁接 → 组合决策 → 红队）**

## 文档与版本

| 文档 | 内容 |
|---|---|
| [PRD.md](PRD.md) | 产品需求文档：用户、目标、功能需求、验收标准 |
| [CHANGELOG.md](CHANGELOG.md) | 版本记录（Keep a Changelog） |
| [docs/RELEASE-NOTES-v0.4.0.md](docs/RELEASE-NOTES-v0.4.0.md) | 本版修改说明与升级指引 |
| [docs/RELEASE-NOTES-v0.3.0.md](docs/RELEASE-NOTES-v0.3.0.md) | v0.3 修改说明（决策模式全流程） |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 贡献指南与发布流程 |

当前版本：**v0.4.0**（行为更新：双模式——灵感模式=品类碰撞房+100 刺激牌+挑号 Gate+筛选房；决策模式=v0.3 全套保留）。

---

## v0.4 有什么不同

v0.3 把脑暴升级成可落地的决策卡引擎；但一道真实产品题（三防平板）连测三轮发现：创意题被收敛纪律挤压，产出“合理但无聊”。v0.4 依据该实测把**发散与收敛拆成两个房间**：

| 维度 | v0.3（仅决策模式） | v0.4 |
|---|---|---|
| 模式 | 单一六步 | 双模式：灵感（创意题默认）+ 决策（原六步保留） |
| 发散源 | 66 机制领域牌 | 灵感：100 品类刺激牌/11 世界（品类距离最大化）；决策：66 机制牌 |
| 发散纪律 | 机制卡+失效前提（审查在发散中） | 碰撞房零禁词（成本/BOM/可行性/风险/认证），审查器一律后置 |
| 产出形态 | 8 候选+3 落地卡 | 灵感：12-15 组四行碰撞组（品类→属性→嫁接→爽点）→ 用户挑号 → Top-3 卡 |
| 收敛方式 | 打分+门槛 | Gate 只报编号不推荐；筛选房有用性三问+可行性阶梯（L0-L3，L2 必给 1/10 降级版） |
| 用户位置 | 被动接收 Top3 | 主动挑号；否决信号回灌过滤器，否过的类型不回潮 |
| 评测 | 7 case+G11/G12 | 8 case（含灵感题）+G13+4 数换算（碰撞组数/可用率/存活率/类型回潮） |
| 决策模式 | — | 与 v0.3.0 完全一致，未动 |

---

## 它解决什么问题

很多 product brainstorm 低效，不是因为团队不努力，而是因为大家的思路都被困在同一个行业框架里：

- 点子越想越像同行
- 方案越聊越保守
- 一开会就讨论可行性
- 还没发散，就开始否定
- 最后选出的“Top 3”是三个安全但相似的功能

`跨域迁移脑暴` 的作用，是强行打破这种局面：从别的行业/系统/领域借**底层解法**，而不是抄表面功能；再用机制卡、结构映射和红队，把“听起来很妙”变成“说得清、测得了”。

---

## 什么时候用

**灵感模式**（创意题）：

- “帮我创意几组，准备做一个××”
- “要炸一点的新方向，别给我行业内的常规解”
- “先看创意，可行性后面再说”

**决策模式**（落地题）：

- 现有方案同质化，被行业惯性锁死，且要推进落地
- 需要说清“这个点子借了什么机制、为什么可能成立”
- 带预算/否决者/执行人约束的运营或功能题
- 团队共创/工作坊，需要发散 + 收敛的完整流程

高匹配表达：

- “帮我跨界脑暴一下”
- “用别的行业机制想新功能”
- “当前脑暴卡住了，帮我炸点新想法”
- “想跳出行业内卷，借别的领域机制看看”
- “帮我做功能/交互/模式创新，多给几个方向”

判不准时默认灵感模式——先给创意，再谈落地。

## 什么时候不用

- 深度行业研究、竞品报告、市场规模测算
- 替用户做最终战略拍板/预算决策
- 用户只想要 1 个直接建议/明确答案
- 已经有明确方案，只需要执行、排期或 PRD
- 纯文案、文章、标题

如果用户给的是**方案**（“我要个提醒”），skill 会先做一次“问题解码”，再开始。

---

## 两种模式 × 两种速度

| | Quick（默认） | Deep |
|---|---|---|
| 灵感模式 | 25-35 分钟；12-15 组碰撞组 + 挑号 + Top-3 卡 | 60-90 分钟；40-60 组 |
| 决策模式 | 20-25 分钟；8 候选 + 3 张落地卡 + 两门 + 三查 | 60-90 分钟；15-18 候选 + 决策 memo |

灵感模式适合创意题、聊天破局、单人快跑；决策模式适合工作坊、高风险、要买账、要落地。门槛和测试在两种模式下都不能省。

---

## 快速开始

把整个目录作为 skill 安装到你的 agent runtime（确保 `SKILL.md` 在 skill 根目录），然后直接说：

> “帮我创意几组，准备做一个阔直板三防机。”（→ 灵感模式）

或者：

> “我们做 AI 笔记 App，用户记完不回看。帮我做一次跨域脑暴，给我几个值得推进的方向。”（→ 决策模式）

灵感模式会：

1. 判模式：创意题 → 碰撞房；brief 只留题面/人群/软偏好
2. 抽 12-15 张品类刺激牌（≥5 世界，距离拉满）
3. 出 12-15 组碰撞组（品类→属性→嫁接→爽点），弃牌写死因
4. 你挑编号（AI 只报号不推荐）；否过的类型下一批消失
5. 挑中的进筛选房：有用性三问 + 可行性阶梯 + show-stopper
6. Top-3 出七行落地卡；要立项转决策模式补红队

决策模式会：

1. 解码问题，写一句 brief；收三个数+否决者
2. 标目标的结构坐标
3. 抽 3 个结构异质领域（含 wildcard）
4. 提炼机制卡（带失效前提）
5. 做结构映射，生成 8 个候选
6. 选 safe/bold/wildcard 组合，过成本/容量门，每个带便宜实验
7. 过红队，给出下一步

---

## 它和普通 brainstorm 的区别

### 1. 迁移机制，不搬功能

不是“给笔记加经验条”，而是“小任务 → 即时反馈 → 累积 → 解锁”的因果回路。

### 2. 距离要解释

不是“越远越好”，而是“结构不同 + 能桥接”。用结构三轴（集中/同步/验证）避免“行业标签异质”。

### 3. 机制要可证伪

每张机制卡必须写“失效前提”：若＿不成立，它退化为＿。写不出，就是功能。

### 4. 嫁接要结构对应

来源要素 → 目标要素 → 保持的关系 → 断裂的假设 → 谁验证反馈。不是修辞类比。

### 5. 组合 > 排名

不选三个最高分，而选 safe / bold / wildcard；每个下注带最危险假设、便宜实验、阈值、kill 条件。

### 6. 伦理是门槛

操纵、成瘾、隐私、歧视、安全：一票否决或 redesign，不靠“用户接受度高”放行。

---

## 文件结构

```text
cross-domain-brainstorm/
├── SKILL.md
├── README.md
├── PRD.md                           # 产品需求文档
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── docs/
│   ├── RELEASE-NOTES-v0.2.1.md      # v0.2.1 修改说明
│   ├── RELEASE-NOTES-v0.3.0.md      # v0.3 修改说明
│   └── RELEASE-NOTES-v0.4.0.md      # 本版修改说明
├── references/
│   ├── collision-room.md            # 灵感模式·碰撞房规则（禁词/弃牌/扩容器/元模式）
│   ├── triage-room.md               # 灵感模式·筛选房（有用性三问/可行性阶梯/show-stopper）
│   ├── stimulus-library.md          # 品类刺激库 100 张/11 世界
│   ├── domain-library.md            # 决策模式·距离模型 + 66 领域牌堆 + 5 标签/3 硬规则
│   ├── mechanism-examples.md        # 机制卡 + 5 个检验 + 样例
│   ├── grafting.md                  # 结构映射 + 决赛表面检查 + 组合/负向迁移
│   ├── convergence.md               # 反平庸三问 + 门槛 + 两门 + 落地卡 + 先例三查
│   ├── red-team.md                  # 伦理/现状/验证容量/二阶效应/高风险
│   ├── facilitation.md              # 团队工作坊协议
│   ├── output-templates.md          # 灵感/决策 × Quick/Deep 模板
│   ├── example-session.md           # AI 笔记 App 完整演练（v0.2 机制演示）
│   └── example-session-hardware.md  # 老人智能家居完整演练（v0.2 机制演示）
├── assets/
│   ├── domain-deck.json             # 66 领域结构化数据（18 张带标签）
│   └── stimulus-deck.json           # 100 品类刺激牌结构化数据
├── scripts/
│   ├── domain_sampler.py            # 确定性抽样（双 deck：机制领域 + 品类刺激）
│   ├── validate_skill.py            # 包校验
│   └── package.ps1                  # 重新打包 zip
├── evals/
│   ├── cases.md                     # 8 个评测 case（含运营题 + 灵感题）
│   ├── rubric.md                    # 7 维 rubric + G1-G13 门槛 + 2 字段
│   └── run.md                       # A/B 协议
└── .github/workflows/ci.yml         # 校验 + markdown lint
```

---

## 抽样脚本（可选）

`scripts/domain_sampler.py` 是一个纯标准库的确定性抽样器，双 deck。

**决策模式**（66 机制领域牌）：

```bash
python scripts/domain_sampler.py --target "AI 笔记" \
  --axis substrate=digital --axis centralization=distributed \
  --axis sync=episodic --axis risk=low --axis resource=abundant \
  --axis verification=self_reported --axis agent=individual \
  --seed 42
```

输出 3 个领域（2 个高距离 + 1 个 wildcard），带距离轴、结构差异、桥接提示和机制。

**灵感模式**（100 品类刺激牌）：

```bash
python scripts/domain_sampler.py --stimulus --stim-count 13 --seed 42
# 题面是军品气质时，可减抽相近世界、排除另一个：
python scripts/domain_sampler.py --stimulus --stim-count 13 --near-world military --ban-world toybox
```

输出带编号的刺激牌表（#/品类/世界/类型/属性/一句话机制），覆盖 ≥5 世界、同世界不相邻。

脚本只是“抽牌器”，不替代判断；桥、机制、验证仍要人来写。

---

## 示例

- [AI 笔记 App](references/example-session.md)：低风险、数字、个人；演示如何淘汰“经验条/AI 摘要/每日提醒”，用分诊/审计/免疫系统生成“决策票据/风险票据/记忆集”等。
- [老人智能家居](references/example-session-hardware.md)：高风险、物理、多利益相关者；演示如何用检查单/交接班/日课，避免“更多摄像头/健康评分”。

---

## 评测

`evals/` 提供 8 个 case（含运营题 + 灵感题）、7 维 rubric + G1-G13 门槛、A/B 协议。

```bash
python scripts/validate_skill.py
python scripts/domain_sampler.py --self-test
```

CI 会跑：

- 包结构/链接/表格校验
- 领域 deck schema
- 抽样器自测
- markdown lint

---

## 安装

1. 克隆/下载本目录。
2. 放到你的 agent runtime 的 skills 目录（例如 Claude Skills 的 `skills/cross-domain-brainstorm/`）。
3. 确保 `SKILL.md` 在 skill 根目录，`references/`、`assets/` 同级。
4. 重启/刷新会话，让 skill 被加载。

不同 runtime 的安装路径不同；核心要求只有一条：`SKILL.md` 在 skill 根目录，引用的相对路径存在。

---

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。

改动行为前，先跑：

```bash
python scripts/validate_skill.py
python scripts/domain_sampler.py --self-test
```

如果你改了输出格式/流程，附一个 before/after 的 eval 记录。

---

## License

MIT。见 [LICENSE](LICENSE)。

---

## English summary

`cross-domain-brainstorm` is a cross-domain ideation skill with **two modes**. **Inspiration mode** (default for creative briefs): collide the product with 100 category-stimulus cards across 11 worlds — ideas first, feasibility later; forbidden words (cost/BOM/feasibility/risk/certification) keep reviewers out of the divergence room; the user picks numbers at the Gate (no recommendations), then a triage room applies the usefulness three-questions and a feasibility ladder (L0 software → L3 research, with mandatory 1/10-scale downgrades for mechanisms). **Decision mode** (unchanged since v0.3): transfer **causal mechanisms** — trigger → feedback → causal chain → failure precondition — sample structurally distant domains, separate divergence from convergence, and land a **safe / bold / wildcard** portfolio as decision cards with owners, budgets, and kill conditions.

**Speeds**: Inspiration Quick (~25-35 min, 12-15 mashups), Inspiration Deep (~60-90 min, 40-60); Decision Quick (~20-25 min, 8 ideas + 3 landing cards), Decision Deep (~90 min).

**Core principles**: ideas before feasibility (inspiration) / mechanisms, not features (decision); require a failure precondition; separate divergence from convergence; rejected types never come back; ethics as a gate.

**Repo layout**: `SKILL.md` is the entry point; `PRD.md` documents goals, requirements, and acceptance criteria; `references/` contains the collision/triage rooms, the stimulus library, the domain deck, mechanism cards, grafting, convergence, red team, facilitation, templates, and two full worked examples; `assets/` holds both machine-readable decks; `evals/` contains 8 cases, a 7-dimension rubric with G1-G13 gates, and an A/B protocol; release notes live under `docs/`.

**Install**: place this folder in your agent's skills directory, with `SKILL.md` at the skill root. See [README.md](README.md) for details.

**License**: MIT.
