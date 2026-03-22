# notionhomeworkmanager

Notionの課題・持ち物・報酬データベースを自動管理するPythonツールです。  
毎日深夜0時（JST）に GitHub Actions で自動実行され、期限切れ・完了済みのエントリを「終了」としてマークします。

---

## 機能

- 期限切れかつ完了済みの **課題・持ち物** エントリを自動で「終了」に更新
- 完了済みの **報酬** エントリを自動で「終了」に更新
- GitHub Actions による毎日の自動実行（JST 0:00）
- `workflow_dispatch` によるGitHub UI / API からの手動実行にも対応

---

## 動作条件

| 項目 | バージョン |
|------|-----------|
| Python | 3.9 以上（推奨: 3.12） |
| notion-client | 2.7.0 以上 |

---

## セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/<your-username>/notionhomeworkmanager.git
cd notionhomeworkmanager
```

### 2. 依存パッケージをインストール

```bash
rye sync
```

### 3. 環境変数を設定

`.env` ファイルをプロジェクトルートに作成し、以下を記述します。

```env
NOTION_API_KEY=your_notion_integration_token
NOTION_DATA_SOURCE_ID=your_notion_database_id
```

| 変数名 | 説明 |
|--------|------|
| `NOTION_API_KEY` | Notion インテグレーションのAPIキー |
| `NOTION_DATA_SOURCE_ID` | 管理対象のNotionデータベースID |

> **Notion APIキーの取得方法**  
> [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations) からインテグレーションを作成し、トークンをコピーしてください。  
> また、対象データベースのページでインテグレーションを「接続先」として追加する必要があります。

### 4. スクリプトを実行

```bash
python ./src/notionhomeworkmanager/main.py
```

---

## Notionデータベースの構成

このツールは以下のプロパティを持つNotionデータベースを前提としています。

| プロパティ名 | 種類 | 説明 |
|-------------|------|------|
| `期限` | 日付 | 課題・持ち物の締め切り日 |
| `完了` | チェックボックス | 完了したらチェック |
| `終了` | チェックボックス | このツールが自動でONにする（アーカイブ扱い） |
| `種類` | セレクト | `課題` / `持ち物` / `報酬` のいずれか |

---

## 更新ロジック

以下の条件に合致するエントリの `終了` プロパティを `true` に更新します。

```
（課題 または 持ち物）かつ 期限切れ かつ 完了済み かつ 未終了
または
報酬 かつ 完了済み かつ 未終了
```

---

## GitHub Actions による自動実行

### 自動スケジュール実行

毎日 **JST 0:00**（UTC 15:00）に自動実行されます。

```yaml
schedule:
  - cron: '0 15 * * *'
```

### GitHub Secretsの設定

リポジトリの **Settings → Secrets and variables → Actions** に以下を登録してください。

| Secret名 | 値 |
|----------|----|
| `NOTION_API_KEY` | NotionのAPIキー |
| `NOTION_DATA_SOURCE_ID` | 対象データベースのID |

### 手動実行

GitHub の **Actions タブ** から `Update Expired and Completed Homeworks` ワークフローを選択し、「Run workflow」ボタンで手動実行できます。

---

## プロジェクト構成

```
notionhomeworkmanager/
├── .github/
│   └── workflows/
│       └── update-homework-workflow.yml  # GitHub Actions ワークフロー
├── src/
│   └── notionhomeworkmanager/
│       ├── __init__.py
│       └── main.py                       # メインスクリプト
├── pyproject.toml
├── requirements.lock
└── README.md
```

---

## ライセンス

MIT License
