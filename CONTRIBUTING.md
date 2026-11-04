# Contributing

感谢你愿意改进 `cross-domain-brainstorm`。

这个项目的目标不是“加更多内容”，而是让跨域机制迁移**更可解释、更可检验、更可证伪**。请优先提交能提高这三点质量的改动。

## 先跑校验

```bash
python scripts/validate_skill.py
python scripts/domain_sampler.py --self-test
```

如果改了 Markdown：

```bash
npx --yes markdownlint-cli2@0.13.0 "SKILL.md" "README.md" "CHANGELOG.md" "CONTRIBUTING.md" "references/*.md" "evals/*.md"
```

如果改了 skill 包内容，重新打包：

```powershell
pwsh -NoProfile -File scripts/package.ps1
```

## 设计原则

1. **SKILL.md 保持轻**：只放入口、流程、门槛、输出契约；细节放 `references/`。
2. **不重复**：同一件事只在一个文件里定义；其他地方引用。
3. **机制优先**：新增内容必须能帮助“写因果链/失效前提/验证者”，而不是增加术语。
4. **可证伪**：每个新方法都要能落到“假设 + 实验 + 阈值 + kill 条件”。
5. **伦理是门槛**：不要提交依赖操纵/成瘾/隐私侵犯/歧视的示例。
6. **中文优先**：保留中文表达的自然度；英文只做摘要。

## 常见改动

### 新增一个领域

1. 在 `assets/domain-deck.json` 加一条，填 7 轴、机制、桥接提示、richness。
2. 在 `references/domain-library.md` 的对应分组表加一行。
3. 运行 `python scripts/validate_skill.py`，确认：
   - 48 个领域；
   - id/name 唯一；
   - 领域名出现在 `domain-library.md`；
   - 抽样器自测通过。

### 新增一个机制样例

1. 放在 `references/mechanism-examples.md`，包含 9 个字段。
2. 必须写“失效前提”和“谁验证反馈”。
3. 附一个低质量对照，说明它为什么过不了五个测试。
4. 不要用“游戏化/平台化/赋能”这类空词。

### 新增一个 eval case

1. 在 `evals/cases.md` 加一个 `## Case N`。
2. 写清：用户、问题、现状、约束、成功指标、non-goals、常见陷阱、好输出信号。
3. 至少覆盖一种新场景（数字/物理/高风险/公共服务/团队）。
4. 在 `evals/run.md` 的样本计划里说明是否加入主评测。

### 改动流程/输出格式

1. 更新 `SKILL.md` 和受影响的 `references/`。
2. 更新 `CHANGELOG.md`。
3. 附一个 before/after 的 eval 记录（至少 3 个 case）。
4. 如果只是文字澄清，不需要 eval；如果是行为变化，需要。

## 版本与兼容

- 遵循 semver：`0.2.x` 是兼容修补；`0.3.0` 是行为变化；`1.0.0` 是稳定接口。
- 保留现有文件名；新增文件优先，不要随意重命名。
- 删除/重命名文件时，在 `CHANGELOG.md` 写 migration note。
- 不要手改 `cross-domain-brainstorm.zip`；用 `scripts/package.ps1` 重新生成。

## PR 检查清单

- [ ] `python scripts/validate_skill.py` 通过
- [ ] `python scripts/domain_sampler.py --self-test` 通过
- [ ] `npx --yes markdownlint-cli2@0.13.0 "SKILL.md" "README.md" "CHANGELOG.md" "CONTRIBUTING.md" "references/*.md" "evals/*.md"` 通过（如本地可用）
- [ ] `CHANGELOG.md` 已更新
- [ ] 新增/修改的链接可打开
- [ ] 没有把“功能”写成“机制”
- [ ] 没有放行操纵/成瘾/隐私侵犯的示例
- [ ] 如果改了行为，附 eval 记录

## License

提交即表示你同意以 MIT License 发布你的贡献。
