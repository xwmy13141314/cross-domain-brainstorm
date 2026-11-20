# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog principles.

## [Unreleased]

### Added

- Reserved for upcoming changes.

## [v0.3.0] - 2026-11-19

Behavior update driven by a 4-bot red-team field evaluation (chain-restaurant ops 13/25, greenhouse agriculture 14/25, eldercare ops 14/25, structural review). Core shift: from "ideas + mechanism cards" to **landable decision cards**.

### Added

- Step 0 problem-type branch (product/experience vs ops/execution) with three numbers (budget cap / executor minutes / verifier capacity) plus a named vetoer; unknowns must be labeled, never fabricated.
- Three 7-line landing cards (existing alternative / what it fails at / mechanism + failure precondition / cheapest test / scaled cost range + unknowns / who pays-executes-embeds / kill + stop signal); a card that cannot be filled keeps the idea out of the portfolio.
- Two Pass/Fail gates applied only to the 3 finalist bets: cost fit and capacity fit, with "shrink scope once, then kill" handling; wildcard passes on probe cost (1/10 budget or one person-day).
- Mandatory precedent check (competitors / public cases / platform-or-patent) with search scope, date, evidence grade; "未查" allowed, fabrication forbidden.
- Domain library 48→66: +10 low-resource & informal-economy domains, +8 agriculture/food/supply-chain domains; 5 tags (resource / power / observation / verifier capacity / example) and 3 hard sampling rules (≥1 low-resource card for low-resource targets; ≤1 example card; target-industry cards banned).
- `evals/cases.md` Case 7 (eldercare service quality, ops case with the three numbers and vetoer); `evals/rubric.md` G11/G12 gates + 2 required fields (adoption ownership, precedent evidence grade); `evals/run.md` switched to v0.2-vs-v0.3, Quick cap 25 min, fabricated precedents auto-fail.

### Changed

- Quick: 15→20-25 min, 10→8 ideas (6 regular + 1 A×B + 1 negative transfer; 1/10-scale variant mandatory). Per-idea five surface-copy tests dropped (finalists only, once each); decision log dropped.
- Anti-mediocrity test reanchored from "covered by an existing product" to the three questions (how is it done today / what does that fail to do / what does the new idea spend more and less of) — fixes both the SOP-blind spot on ops problems and the false kill of "old form, new structure".
- Red team: verifier questions 4→8 (capacity source, overflow triage, right to refuse/escalate); high-risk list extended to food/agrochemicals/chemicals/frontline-worker safety; red light = one redesign, then kill.
- `scripts/domain_sampler.py`: 66 cards, low-resource guarantee, example-card cap. `scripts/validate_skill.py`: VERSION 0.3.0, deck 66, ≥7 eval cases incl. ops case, v0.3 anchor checks.
- Optional scoring 0-2 → 1-5 with anchors; feasibility/acceptability excluded from totals.

## [v0.2.1] - 2026-11-05

Documentation and release-engineering patch. **No behavior changes**: the v0.2.0 workflow, quality gates, and output contract are unchanged.

### Added

- `PRD.md`: product requirements document covering background, users, goals/non-goals, 13 functional requirements (FR-1 … FR-13), non-functional requirements, user flows, acceptance criteria, metrics, release policy, risks, and open questions.
- `docs/RELEASE-NOTES-v0.2.1.md`: user-facing change notes and upgrade steps; `docs/` reserved for future release notes and migration guides.

### Changed

- `README.md`: version bumped to v0.2.1; new "文档与版本" section linking PRD / CHANGELOG / release notes / CONTRIBUTING; file map now includes `PRD.md` and `docs/`.
- `CHANGELOG.md`: added the `[v0.2.1]` entry.
- `SKILL.md`: frontmatter `version: 0.2.1`, `updated: 2026-11-05`; title updated.
- `assets/domain-deck.json`: `version: 0.2.1`, `updated: 2026-11-05`.
- `scripts/validate_skill.py`: single `VERSION` constant now drives checks; requires `PRD.md` and `docs/RELEASE-NOTES-v0.2.1.md`; validates `SKILL.md` frontmatter version and deck version against `VERSION`.
- `scripts/package.ps1`: now packages `PRD.md` and `docs/`; `cross-domain-brainstorm.zip` regenerated.
- `CONTRIBUTING.md`: markdownlint command extended to `PRD.md` and `docs/*.md`; PR checklist adds a documentation-sync item.

## [v0.2.0] - 2026-11-04

### Added

- `SKILL.md` rewritten as a mechanism-transfer engine with a six-step workflow:

  frame → distance axes → domain sampling → mechanism cards → structural grafting → portfolio + red team.

- Two modes: **Quick** (~15 min, ~10 ideas) and **Deep** (~60-90 min, 15-18 ideas).
- New `references/domain-library.md` with a structural distance model (centralization / sync / verification), contextual axes, a 48-domain deck, sampling rules, and a domain ledger.
- New `assets/domain-deck.json` as the machine-readable domain deck.
- New `references/mechanism-examples.md` with the 9-field mechanism card, the trigger/feedback/failure-precondition triad, five mechanism tests, and six worked examples.
- New `references/grafting.md` with the structural mapping table, five surface-copy tests, forced variation menu, A×B combination matrix, and negative transfer.
- New `references/convergence.md` with the anti-mediocrity test, four gates, safe/bold/wildcard portfolio, hypothesis/assumption/test/threshold/kill fields, and cheapest-falsification ranking.
- New `references/red-team.md` with ethics, status quo, verification, second-order effects, reversibility, stakeholder mapping, and high-stakes rules.
- New `references/facilitation.md` with a 90-minute and a 45-minute team workshop protocol, silent writing, round-robin, build-and-jump, dot voting, pre-mortem, and remote/async variants.
- New `references/example-session-hardware.md` for a non-AI, physical, high-stakes case (elderly smart home).
- New `scripts/domain_sampler.py` (pure standard library) for deterministic domain sampling from a 7-axis target profile.
- New `scripts/validate_skill.py` for frontmatter, references, links, domain deck, eval cases, markdown tables, and sampler self-test.
- New `scripts/package.ps1` to rebuild `cross-domain-brainstorm.zip`.
- New `evals/cases.md` (6 cases), `evals/rubric.md` (7 dimensions + 10 gates), and `evals/run.md` (blind A/B protocol).
- New `.github/workflows/ci.yml`, `.markdownlint.json`, `.markdownlintignore`, and `.gitignore`.

### Changed

- `references/output-templates.md` rewritten for Quick/Deep output, mechanism cards, idea cards, portfolio table, red-team card, and decision memo.
- `references/example-session.md` rewritten around a new AI note-taking case: problem decoding, structural domains (ER triage / audit / immune system), mechanism cards, mapping, 10 ideas, portfolio, red team.
- `README.md` rewritten as a bilingual (Chinese + English summary) project page with install, modes, file map, eval, and contribution notes.
- `SKILL.md` frontmatter now includes `version: 0.2.0`, `updated: 2026-11-04`, and `license: MIT`.
- Domain model changed from "traditional / AI / service" categories to **structural axes** (centralization, sync, verification) plus contextual axes.
- Convergence changed from four equal 0-2 scores + Top 3 to **anti-mediocrity + gates + safe/bold/wildcard portfolio + cheapest falsification**.
- Team mode changed from a host script to a timeboxed facilitation protocol.

### Removed

- The old four-dimension 0-2 scoring as the primary selection mechanism (kept only as optional 1-5 auxiliary scoring).
- The old "at least 6 ideas" ceiling; replaced by Quick 10 / Deep 15-18 with forced variations and combination.
- The old static 32-domain list; replaced by the 48-domain structured deck.
- The stale `cross-domain-brainstorm.zip` is regenerated by `scripts/package.ps1` (do not edit the zip by hand).

### Fixed

- Resolved the contradiction between "not for judging which solution is best" and the old Top 3 step by defining the skill as candidate comparison/portfolio selection, not final strategic decision-making.
- Fixed step-number drift between `SKILL.md` and the example session.
- Added a "solution decoding" step for users who ask for a feature instead of describing the pain.
- Added verification/accountability checks for mechanisms whose feedback is self-reported.

## [v0.1.0] - 2026-04-13

### Added

- Initial public release of the `cross-domain-brainstorm` Claude skill.
- Added `SKILL.md` with a lightweight workflow for cross-domain ideation through mechanism transfer.
- Added `references/domain-library.md` with cross-domain field libraries and sampling guidance.
- Added `references/mechanism-examples.md` with high-quality vs low-quality transfer examples.
- Added `references/output-templates.md` with output formats for ideation, Top 3 selection, solo mode, and team facilitation.
- Added `references/example-session.md` with a complete worked example based on an AI note-taking app.
- Added repository `README.md` for public GitHub presentation.
- Added packaged artifact `cross-domain-brainstorm.zip` for direct distribution.

### Notes

- This version focuses on a practical, lightweight workflow rather than a heavy workshop-style process.
- Suitable for product innovation, feature ideation, interaction exploration, and service-mode brainstorming.
- Not intended for deep research, root-cause analysis, PRD finalization, or long-form writing.
