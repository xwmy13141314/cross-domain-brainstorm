# 跨域迁移脑暴 v0.3.0

A cross-domain ideation skill that transfers **causal mechanisms**, not surface features — and lands them as **decision cards** with owners, budgets, and kill conditions.

一个用于产品/功能/交互/服务/运营流程创新的跨域脑暴 skill：从结构异质的领域借“因果机制”，严格映射到目标问题，最后给出一个小组合的、可被证伪、可落地的下注。

它不靠“看竞品、做组合”，而是靠：

> **题型判定 → 问题解码 → 距离采样 → 机制卡 → 结构嫁接 → 组合决策（落地卡+成本容量门）→ 红队**

## 文档与版本

| 文档 | 内容 |
|---|---|
| [PRD.md](PRD.md) | 产品需求文档：用户、目标、功能需求、验收标准 |
| [CHANGELOG.md](CHANGELOG.md) | 版本记录（Keep a Changelog） |
| [docs/RELEASE-NOTES-v0.3.0.md](docs/RELEASE-NOTES-v0.3.0.md) | 本版修改说明与升级指引 |
| [CONTRIBUTING.md](CONTRIBUTING.md) | 贡献指南与发布流程 |

当前版本：**v0.3.0**（行为更新：题型分支、三个数+否决者、3 张落地卡、成本/容量 Pass/Fail 门、先例三查、领域库 48→66、Quick 20-25 分钟）。

---

## v0.3 有什么不同

v0.2 把脑暴升级成可追溯、可检验的机制迁移引擎；v0.3 依据 4 个独立 bot 的行业实测（餐饮/农业/养老），把输出从“创意+评分”升级为**可落地的决策卡**。

| 维度 | v0.2 | v0.3 |
|---|---|---|
| 题型 | 默认产品题 | Step 0 分支：产品/体验 vs 运营/执行 |
| 约束 | 硬约束只在框定提 | 三个数（预算/执行分钟/验证容量）+否决者，全流程回检 |
| 创意 | 10 个 | 8 个（6+A×B+负向；1/10 版必选），决赛才做表面检查 |
| 收敛 | 反平庸一句话 + 四门槛 | 反平庸三问 + 四门槛 + 成本/容量 Pass/Fail 门（超限先缩一次） |
| 交付 | Top3 + 评分表 | 3 张 7 行落地卡（谁买单/谁执行/嵌哪一步/kill 信号） |
| 先例 | 无 | 强制三查（竞品/案例/专利），写检索范围+日期+证据等级，未查可标、编造禁止 |
| 领域 | 48 张 | 66 张（+10 低资源/非正规、+8 农业/食品供应链）+5 标签+3 硬规则 |
| 反平庸 | 锚“现有产品” | 三问锚“现有做法/SOP”，不再误杀“形式旧结构新” |
| 红队 | 验证者 4 问 | 8 问（含容量来源/超载处置）；高风险加食品/农残/工人安全；红灯 redesign 一次 |
| 评测 | 6 case | 7 case（含养老运营题）+ G11/G12 门 + 2 字段 |

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

- 现有方案同质化，明显被行业惯性锁死
- 脑暴卡住，需要结构性刺激
- 想要多个候选，而不是一个直接建议
- 需要说清“这个点子借了什么机制、为什么可能成立”
- 团队共创/工作坊，需要发散 + 收敛的完整流程

高匹配表达：

- “帮我跨界脑暴一下”
- “用别的行业机制想新功能”
- “当前脑暴卡住了，帮我炸点新想法”
- “想跳出行业内卷，借别的领域机制看看”
- “帮我做功能/交互/模式创新，多给几个方向”

## 什么时候不用

- 深度行业研究、竞品报告、市场规模测算
- 替用户做最终战略拍板/预算决策
- 用户只想要 1 个直接建议/明确答案
- 已经有明确方案，只需要执行、排期或 PRD
- 纯文案、文章、标题

如果用户给的是**方案**（“我要个提醒”），skill 会先做一次“问题解码”，再开始。

---

## 两种速度

| | Quick（默认） | Deep |
|---|---|---|
| 时间 | 约 20-25 分钟 | 60-90 分钟 |
| 领域 | 3 个 | 5 个 |
| 机制 | 3 张卡 | 3-5 张卡 |
| 候选 | 8 个（6+A×B+负向） | 15-18 个 |
| 交付 | 2 页 + 3 张落地卡 + 两门 + 三查 | 4 页 + 决策 memo + 利益相关者 + pre-mortem |
| 适合 | 聊天、单人、快速破局、运营试点 | 工作坊、高风险、需要买账 |

Quick 不是“简化版的方法”，而是“同样的方法，少填几张表”。门槛和测试不能省。

---

## 快速开始

把整个目录作为 skill 安装到你的 agent runtime（确保 `SKILL.md` 在 skill 根目录），然后直接说：

> “我们做 AI 笔记 App，用户记完不回看。帮我做一次跨域脑暴，给我几个值得推进的方向。”

或者更具体：

> “我们做老人智能家居，子女想监控但老人抗拒。帮我用跨域机制找几个不侵犯隐私的方向。”

Skill 会：

1. 解码问题，写一句 brief
2. 标目标的结构坐标
3. 抽 3 个结构异质领域（含 wildcard）
4. 提炼机制卡（带失效前提）
5. 做结构映射，生成 10 个左右候选
6. 选 safe/bold/wildcard 组合，每个带便宜实验
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
│   └── RELEASE-NOTES-v0.3.0.md      # 本版修改说明
├── references/
│   ├── domain-library.md          # 距离模型 + 66 领域牌堆 + 5 标签/3 硬规则
│   ├── mechanism-examples.md      # 机制卡 + 5 个检验 + 样例
│   ├── grafting.md                # 结构映射 + 决赛表面检查 + 组合/负向迁移
│   ├── convergence.md             # 反平庸三问 + 门槛 + 两门 + 落地卡 + 先例三查
│   ├── red-team.md                # 伦理/现状/验证容量/二阶效应/高风险
│   ├── facilitation.md            # 团队工作坊协议
│   ├── output-templates.md        # Quick/Deep 模板
│   ├── example-session.md         # AI 笔记 App 完整演练（v0.2 机制演示）
│   └── example-session-hardware.md# 老人智能家居完整演练（v0.2 机制演示）
├── assets/
│   └── domain-deck.json           # 66 领域结构化数据（18 张带标签）
├── scripts/
│   ├── domain_sampler.py          # 确定性领域抽样（低资源保障/示例限额）
│   ├── validate_skill.py          # 包校验
│   └── package.ps1                # 重新打包 zip
├── evals/
│   ├── cases.md                   # 7 个评测 case（含运营题）
│   ├── rubric.md                  # 7 维 rubric + G1-G12 门槛 + 2 字段
│   └── run.md                     # A/B 协议
└── .github/workflows/ci.yml       # 校验 + markdown lint
```

---

## 领域抽样（可选脚本）

`scripts/domain_sampler.py` 是一个纯标准库的确定性抽样器，读取 `assets/domain-deck.json`：

```bash
python scripts/domain_sampler.py --target "AI 笔记" \
  --axis substrate=digital --axis centralization=distributed \
  --axis sync=episodic --axis risk=low --axis resource=abundant \
  --axis verification=self_reported --axis agent=individual \
  --seed 42
```

输出 3 个领域（2 个高距离 + 1 个 wildcard），带距离轴、结构差异、桥接提示和机制。

Deep 模式：

```bash
python scripts/domain_sampler.py ... --count 5 --anti-domain
```

脚本只是“抽牌器”，不替代判断；桥、机制、验证仍要人来写。

---

## 示例

- [AI 笔记 App](references/example-session.md)：低风险、数字、个人；演示如何淘汰“经验条/AI 摘要/每日提醒”，用分诊/审计/免疫系统生成“决策票据/风险票据/记忆集”等。
- [老人智能家居](references/example-session-hardware.md)：高风险、物理、多利益相关者；演示如何用检查单/交接班/日课，避免“更多摄像头/健康评分”。

---

## 评测

`evals/` 提供 6 个 case、7 维 rubric、A/B 协议。

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

`cross-domain-brainstorm` is a cross-domain ideation skill. Instead of copying features from other industries, it transfers **causal mechanisms**: trigger → feedback → causal chain → failure precondition. It samples structurally distant domains (not just different industry labels), maps source elements to target elements, separates divergence from convergence, and selects a portfolio of **safe / bold / wildcard** bets, each with a falsifiable assumption and a cheap test.

**Modes**: Quick (~15 min, ~10 ideas) and Deep (~90 min, 15-18 ideas).

**Core principle**: transfer mechanisms, not features; require a failure precondition; verify the feedback signal; put ethics before scoring.

**Repo layout**: `SKILL.md` is the entry point; `PRD.md` documents goals, requirements, and acceptance criteria; `references/` contains the domain deck, mechanism cards, grafting, convergence, red team, facilitation, templates, and two full worked examples; `evals/` contains 6 cases, a 7-dimension rubric, and an A/B protocol; release notes live under `docs/`.

**Install**: place this folder in your agent's skills directory, with `SKILL.md` at the skill root. See [README.md](README.md) for details.

**License**: MIT.
