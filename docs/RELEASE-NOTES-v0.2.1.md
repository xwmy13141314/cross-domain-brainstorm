# Release Notes：v0.2.1

| 项目 | 内容 |
|---|---|
| 版本 | **0.2.1** |
| 发布日期 | 2026-11-05 |
| 类型 | 文档与发布层更新（patch） |
| 行为变化 | 无；v0.2.0 的流程、质量门、输出契约保持不变 |
| 上一版本 | [v0.2.0](#v020) |

---

## 1. 一句话

v0.2.1 不改变 skill 的行为，只把 **PRD、README、修改说明、版本号、校验与打包**补齐，让这个 skill 从“能用”变成“可维护、可发布、可验收”。

## 2. 本版新增

- **`PRD.md`**：产品需求文档，包含背景、用户、目标/非目标、13 条功能需求、非功能需求、用户流程、验收标准、指标、发布策略、风险与开放问题。
- **`docs/RELEASE-NOTES-v0.2.1.md`**：本文件，面向使用者和贡献者的修改说明。
- **`docs/` 目录**：为后续版本说明、迁移指南、设计记录留位置。

## 3. 本版修改

- `README.md`：
  - 标题升级为 v0.2.1；
  - 增加“文档与版本”入口，链接 PRD、CHANGELOG、Release Notes；
  - 文件结构加入 `PRD.md`、`docs/`；
  - English summary 同步版本。
- `CHANGELOG.md`：
  - 增加 `[v0.2.1]` 条目；
  - 明确本版是文档/发布层 patch，无行为变化；
  - 保留 v0.2.0 / v0.1.0 历史。
- `SKILL.md`：
  - frontmatter `version: 0.2.1`；
  - `updated: 2026-11-05`；
  - 标题同步 v0.2.1。
- `assets/domain-deck.json`：
  - `version: 0.2.1`；
  - `updated: 2026-11-05`。
- `scripts/validate_skill.py`：
  - 要求 `PRD.md`、`docs/RELEASE-NOTES-v0.2.1.md`；
  - 校验 `SKILL.md` 版本为 `0.2.1`；
  - 校验 domain deck 版本为 `0.2.1`。
- `scripts/package.ps1`：
  - 打包加入 `PRD.md`、`docs/`；
  - 重新生成 `cross-domain-brainstorm.zip`。
- `CONTRIBUTING.md`：
  - 增加“文档更新”检查项：PRD / release notes / CHANGELOG / 版本号同步。
- `cross-domain-brainstorm.zip`：
  - 重新打包，包含 PRD、docs、README、CHANGELOG、references、assets、scripts、evals。

## 4. 兼容性

- **无破坏性变更**：v0.2.0 的 `SKILL.md` 流程、文件路径、输出契约、质量门保持不变。
- 已有安装只需替换目录；不需要改配置。
- 已有调用方不需要改 prompt。
- 版本号从 `0.2.0` 升到 `0.2.1`，属于 semver patch。

## 5. 升级步骤

1. 拉取 `main` 或下载 `v0.2.1` 的 zip。
2. 替换旧的 skill 目录（保留 `SKILL.md` 在根目录）。
3. 不需要改任何配置。
4. 可选：运行校验：

```bash
python scripts/validate_skill.py
python scripts/domain_sampler.py --self-test
```

## 6. 验证

发布前执行：

```bash
python scripts/validate_skill.py
python scripts/domain_sampler.py --self-test
npx --yes markdownlint-cli2@0.13.0 "SKILL.md" "README.md" "CHANGELOG.md" "CONTRIBUTING.md" "PRD.md" "references/*.md" "evals/*.md" "docs/*.md"
```

并执行：

1. 用 `scripts/package.ps1` 重新打包；
2. 解包 zip，在包内运行 `python scripts/validate_skill.py`；
3. 确认 `SKILL.md`、`README.md`、`CHANGELOG.md`、`PRD.md`、`assets/domain-deck.json` 版本号一致。

本版验证结果记录在发布 commit / GitHub Release 中。

## 7. 已知问题 / 下一步

- **真人 A/B 盲评尚未执行**：`evals/` 已就绪，但还没有跑 3 个 case 的 pilot。建议 v0.3 前完成。
- **`SKILL.md` 约 14KB**：如果加载成本是问题，v0.3 可压到 8-9KB，把更多细节下沉到 references。
- **License 仍为 MIT**：如果项目更偏“文档/方法”，可考虑 CC BY 4.0 或双许可；需维护者决定。
- **领域库 48 个**：后续可扩充到 60-80 个，但需要同步 JSON + markdown + validator。

## 8. 相关链接

- [README](../README.md)
- [PRD](../PRD.md)
- [CHANGELOG](../CHANGELOG.md)
- [SKILL.md](../SKILL.md)
- [v0.2.0 变更](../CHANGELOG.md#v020---2026-11-04)

---

## v0.2.0

v0.2.0 是把 v0.1 的“创意提示词”重构为“机制迁移引擎”的行为版本：

- 六步流程：框定 → 距离 → 领域 → 机制卡 → 嫁接 → 组合/红队；
- 结构三轴 + 情境四轴 + 48 领域牌堆；
- 9 字段机制卡 + 失效前提；
- 5 个表面复制测试 + A×B + 负向迁移；
- 反平庸 + 门槛 + safe/bold/wildcard + 最便宜证伪；
- 红队 + 团队 facilitation + 6 个 eval case。

详见 [CHANGELOG v0.2.0](../CHANGELOG.md#v020---2026-11-04)。
