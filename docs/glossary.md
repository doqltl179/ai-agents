---
owns: "Approved rendering of agentkit terms in Korean and Japanese, terms kept as-is, and style choices for the localized READMEs"
volatility: evolving
reviewed: 2026-10-09
---

# Glossary

The single owner of how agentkit terms are written in each README language. Source language: English (`docs.source_locale`). Rules: [translation.md](../core/wiki/workflows/translation.md) «Terminology».

## Terms

`=` means "keep exactly as written in the source".

| Source term (en) | Meaning and context | ko | ja | Notes |
|---|---|---|---|---|
| agentkit | Product name of this kit | = | = | Never translated |
| AI coding agent | The kit's primary reader | AI 코딩 에이전트 | AI コーディングエージェント | |
| kit | This documentation kit | 키트 | キット | |
| single source of truth (SSOT) | One fact, one owning file | 단일 원천(SSOT) | 単一の情報源(SSOT) | Keep the `SSOT` abbreviation after the first use |
| wiki | The rule pages under `core/wiki/` | = | = | |
| role (agent) | An owner defined by an agent card | 역할(agent) | 役割(agent) | |
| role card | The file defining a role | 역할 카드 | 役割カード | |
| skill | An executable procedure | 스킬 | スキル | |
| stack pack | Language, framework, or infra knowledge file | = | = | Kept in English as a kit term |
| surface | The part of a system a role changes | 표면(surface) | 担当領域(surface) | Keep `surface` in parentheses |
| project binding | Paths and stack packs assigned to a role in the profile | 프로젝트 바인딩 | プロジェクトのバインディング | |
| profile | `.ai/project/profile.toml` | 프로필 | プロフィール | |
| overlay | The project-owned `.ai/project/` layer | 오버레이 | オーバーレイ | |
| plane | Governance, execution, quality, evolution | 평면 | プレーン | |
| department | A group of roles | 부서 | 部署 | |
| worktree | A Git worktree for one work unit | 워크트리 | ワークツリー | |
| issue | A hosting-platform issue | 이슈 | Issue | |
| pull request | A hosting-platform pull request | PR | プルリクエスト | |
| promotion | `develop` → `main` pull request at release | 승격(promotion) | 昇格(promotion) | |
| translation | Producing text in another language | 번역 | 翻訳 | |
| tech radar | The watchlist page | = | = | |
| change intake | The kit's change-entry flow | = | = | |

## Style Notes

| Text type | Locale | Register and tone |
|---|---|---|
| README | ko | 합니다체; neutral, concise technical prose |
| README | ja | です・ます体; neutral, concise technical prose |
