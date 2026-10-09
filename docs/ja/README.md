# agentkit

[English](../../README.md) | [한국어](../ko/README.md) | **日本語**

複数のプロジェクトに組み込んで使う **AI コーディングエージェント向けドキュメントキット** です。ルール(wiki)、役割(agent)、手順(skill)、言語・フレームワークの知識(stack pack)を単一の情報源(SSOT)で管理し、Claude Code・Codex・GitHub Copilot・Cursor・Gemini CLI がそれぞれ読み込む形式へ自動生成します。

> キットの文書の第一の読者は **AI エージェント** です。トークン効率とツール互換性のため、エージェント向け文書は英語で書き、報告・コミット・プルリクエストはプロジェクトの言語(`project.language`)に従います。

## 設計

| 原則 | 実現方法 |
|---|---|
| **SSOT** | 一つの事実は一つのファイルだけが所有し、他はリンクのみを張ります。カタログ・セクション索引・ツール別ファイルは元ファイルの frontmatter から **生成** されるため、食い違いが起きません。`check` がリンク切れ、重複した文、古い生成物、インストール済みキットのローカル変更を検出します。 |
| **エージェントのための文書** | すべてのページは `When` / `Route Away When` から始まり、誤って来たエージェントはすぐに離れられます。入口 → セクション索引 → 所有ページの最大 3 段階で答えに到達し、ファイル種別ごとの行数予算が強制されます。 |
| **大企業のような組織** | 管理・実行・品質・進化のプレーンと部署に分かれています。各役割は `Owns` と担当しない作業(それを担当する隣の役割)を明記し、役割が重なりません。 |
| **細分化された役割** | 役割は言語ではなく **担当領域(surface)** で定義し、言語・フレームワークの知識は stack pack で組み合わせます: `役割カード × stack pack × プロジェクトのバインディング` → 例) Next.js フロントエンド担当、FastAPI バックエンド担当、Unity エディタツール担当。プロジェクトは `extends` で役割をさらに絞り込めます。 |
| **スキル** | Issue とプルリクエスト、ワークツリー、リファクタリング、コード・依存関係・スキーマの移行、レビュー観点、ドキュメント、翻訳、キットの導入と進化の手順。スキルは順序だけを持ち、ルールは wiki に置きます。 |
| **過去に留まらない** | すべてのファイルに `volatility` と `reviewed` のメタデータがあり定期的に再検証されます。tech radar がツール・モデル・標準を監視し、change intake で変化を取り込みます。`[scaffold]` ルールはモデルの成長に合わせて整理され、バージョンと移行ノートが各プロジェクトへ届きます。 |

## 作業の流れ

すべての依頼は同じ順序で進みます([request-lifecycle.md](../../core/wiki/operating-model/request-lifecycle.md)):

**依頼内容の確認 → Issue 作成 → `develop` からワークツリー作成 → 作業 → `develop` へのプルリクエスト → 作業中に見つけた Issue の登録**。

`develop` は開発用、`main` はリリース用です。`develop → main` はリリースを依頼されたときの昇格(promotion)プルリクエストでのみ行います。プロジェクトはプロフィールでこの既定値を変更できます。

## 構成

```text
core/                  移植されるキット本体 (プロジェクトでは .ai/kit/ にコピーされ読み取り専用)
  START.md             セッション開始ルーター (AGENTS.md に埋め込まれる)
  wiki/                ルール: principles, operating-model, workflows, evolution, integration, authoring
  agents/<部署>/        役割カード                          (CATALOG.md は自動生成)
  skills/<名前>/        手順                                (CATALOG.md は自動生成)
  stacks/<種類>/        言語・フレームワーク・インフラの知識  (CATALOG.md は自動生成)
  templates/           scaffold テンプレートとプロジェクトプロフィールのスキーマ
tools/agentkit.py      install, update, sync, check, freshness, new
.ai/project/           このリポジトリ自身のオーバーレイ (キットでキットを管理)
```

インストール先プロジェクトの構成とツール別の生成ファイルは [installation.md](../../core/wiki/integration/installation.md) と [tool-adapters.md](../../core/wiki/integration/tool-adapters.md) にあります。カタログ: [役割](../../core/agents/CATALOG.md)、[スキル](../../core/skills/CATALOG.md)、[stack pack](../../core/stacks/CATALOG.md)。

## クイックスタート

必要なもの: Python 3.11 以上(標準ライブラリのみ使用)、Git。GitHub 関連のスキルは `gh` CLI を使います。

```bash
# 1. このリポジトリを取得し、対象プロジェクトにインストール
python tools/agentkit.py install ../my-project --tools claude,codex,copilot

# 2. 対象プロジェクトで .ai/project/profile.toml を編集: 言語、コマンド、有効な役割、パスとスタックのバインディング
#    (各キーの説明は core/templates/project/profile.toml)

# 3. 生成と検証
cd ../my-project
python .ai/kit/tools/agentkit.py sync
python .ai/kit/tools/agentkit.py check
```

手書きの `AGENTS.md` や `CLAUDE.md` がすでにあるプロジェクトでは、`sync` は上書きを拒否します。AI エージェントに **`kit-install` スキル** を実行させると、プロジェクト固有の内容をオーバーレイへ移し、プロフィールを埋めます。

### 更新

```bash
python .ai/kit/tools/agentkit.py update --from https://github.com/doqltl179/ai-agents --ref v0.1.0
```

キットのファイルがローカルで変更されている場合、更新は拒否されます。キットはプロジェクト内では読み取り専用で、改善は `kit-upstream-propose` スキルでこのリポジトリに提案します。

## キットのメンテナンス

このリポジトリを AI ツールで開くと、生成された `AGENTS.md` がキットのメンテナンス用の入口になります(`kit-librarian`、`role-governor`、`trend-scout` などが有効)。

- 元ファイルを編集した後: `python tools/agentkit.py sync` → `python tools/agentkit.py check`
- テスト: `python -m unittest discover -s tools/tests -v`
- 再検証が必要なファイル: `python tools/agentkit.py freshness`
- CI(`.github/workflows/kit-health.yml`): プッシュとプルリクエストごとにテストと `check` を実行し、毎週 freshness を確認して期限切れのファイルがあれば Issue を作成します。
- 進化の手順全体: [evolution/README.md](../../core/wiki/evolution/README.md)

## ライセンス

[MIT](../../LICENSE)
