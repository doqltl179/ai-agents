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

`develop` は開発用、`main` はリリース用です。`develop → main` はリリースを依頼されたときの昇格(promotion)プルリクエストでのみ行います。プロジェクトはプロフィールでこの既定値を変更できます。依頼が複数の作業単位に分かれる場合、エージェントはまず各単位が読み書きする範囲を確認し、別の単位が変更中の文書を参照しないよう順序を決めます。複数の単位を同時に実行する前には、マシンの利用可能なリソース(`agentkit.py capacity`)も確認します。

## プロジェクトへの導入

このリポジトリをプロジェクトにそのままコピーする必要はありません。プロジェクトの**外**の任意の場所に取得して `install` コマンドを実行すると、キット本体だけがプロジェクトにコピーされ、各 AI ツールが読み込むファイルはプロジェクトのルートに生成されます。

> **リポジトリをプロジェクト内に clone してはいけないのですか?** AI ツールは `CLAUDE.md` などの指示ファイルをプロジェクトのルートから読み込むため、サブフォルダに置いたリポジトリはプロジェクトの指示として認識されません。さらに、ツールは作業中に読んだサブフォルダの指示ファイルも取り込みます。このリポジトリの `AGENTS.md` と `CLAUDE.md` はキット自体のメンテナンス用なので、プロジェクトの作業と無関係な指示がセッションに混ざってしまいます。

### 1. インストール

必要なもの: Python 3.11 以上(標準ライブラリのみ使用)、Git。GitHub 関連のスキルは `gh` CLI も使います。

```bash
# プロジェクトの外の任意の場所にキットを取得します(インストール後は削除して構いません)
git clone --depth 1 --branch main https://github.com/doqltl179/ai-agents agentkit

# プロジェクトにインストールします
python agentkit/tools/agentkit.py install path/to/my-project --tools claude,codex,copilot
```

- `main` にはリリース済みのバージョン、`develop` には未リリースの変更があります。バージョンを固定するには、`--branch v<バージョン>` でそのリリースタグを取得します。
- `--tools` でファイルを生成する AI ツールを選びます: `claude`、`codex`、`copilot`、`cursor`、`gemini`。

### 2. 生成されるもの

```text
my-project/
  AGENTS.md, CLAUDE.md      生成されたエントリファイル: ツールがセッション開始時に読み込みます
  .claude/ .codex/ .agents/ .github/…   ツールごとに生成されたエージェント・スキル・ルール
  .ai/kit/                  キット本体(ルール・役割・スキル・stack pack・CLI)、読み取り専用
  .ai/project/              プロジェクトの設定: profile.toml、wiki/、lessons.md
  .ai/generated/            有効な役割とスキルのカタログ
  .gitignore                .ai/tasks/ と .worktrees/ を追加
```

手書きの `AGENTS.md`・`CLAUDE.md`・ツール用ファイルがあれば上書きせずに停止し、その一覧を表示します。内容は次の手順で移します。

### 3. プロジェクトに合わせた設定

AI ツールでプロジェクトを開き、**`kit-install` スキルの実行を依頼**します。このスキルは次のことを行います。

- コードベースを読み取り、`.ai/project/profile.toml` を埋めます: 報告に使う言語、ビルドとテストのコマンド、有効にする役割、役割ごとの担当パスと stack pack。
- 手書きの指示ファイルの内容を `.ai/project/` へ移し、元のファイルは確認を得てから削除します。
- 作業の流れに必要なリポジトリ設定(`develop` ブランチ、デフォルトブランチを `develop` に、マージ済みブランチの自動削除)を提案し、確認を得てから適用します。

手動で設定する場合は `.ai/project/profile.toml` を編集し(各キーの説明は `.ai/kit/core/templates/project/profile.toml` にあります)、`python .ai/kit/tools/agentkit.py sync` を実行します。

### 4. コミット

`.ai/kit/`、`.ai/project/`、`.ai/generated/` と生成ファイル(`AGENTS.md`、`CLAUDE.md`、`.claude/` など)をすべてコミットすると、チーム全員とすべての AI ツールが同じ設定で作業できます。CI に `python .ai/kit/tools/agentkit.py check` を加えると、生成ファイルの手動編集やキットのローカル変更を検出できます。

### 5. 使い方

いつもどおり AI ツールに作業を依頼するだけです。エージェントが `AGENTS.md` を読み、[作業の流れ](#作業の流れ)に従います。スキルを直接実行することもできます(例: Claude Code で `/translate`)。プロジェクト固有の情報は `.ai/project/` にだけ置き、変更したら `sync` を実行します。`.ai/kit/` と生成ファイルは直接編集しません。

### 6. 更新

```bash
python .ai/kit/tools/agentkit.py update
```

既定では、プロフィールの `evolution.upstream`(このリポジトリ)から最新のリリース(`vX.Y.Z` タグ)を取得します。別のバージョンは `--ref <タグまたはブランチ>` で、別の取得元は `--from <URL またはパス>` で指定します。`.ai/kit/` を新しいバージョンに置き換え、現在のバージョン以降の変更点と必要な移行手順を表示してから、ファイルを再生成します。キットのファイルがローカルで変更されている場合は実行を拒否します。キットはプロジェクト内では読み取り専用で、改善は `kit-upstream-propose` スキルでこのリポジトリに提案します。

## リポジトリの構成

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

## キットのメンテナンス

このリポジトリを AI ツールで開くと、生成された `AGENTS.md` がキットのメンテナンス用の入口になります(`kit-librarian`、`role-governor`、`trend-scout` などが有効)。

- 元ファイルを編集した後: `python tools/agentkit.py sync` → `python tools/agentkit.py check`
- テスト: `python -m unittest discover -s tools/tests -v`
- 再検証が必要なファイル: `python tools/agentkit.py freshness`
- CI(`.github/workflows/kit-health.yml`): プッシュとプルリクエストごとにテストと `check` を実行し、毎週 freshness を確認して期限切れのファイルがあれば Issue を作成します。
- 進化の手順全体: [evolution/README.md](../../core/wiki/evolution/README.md)

## ライセンス

[MIT](../../LICENSE)
