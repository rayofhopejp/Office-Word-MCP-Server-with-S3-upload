# AWS環境へのデプロイとGenerative AI Usecases JPでの利用方法

## 概要

このガイドでは、Office-Word-MCP-ServerをAWS環境にデプロイし、作成したWordファイルを自動的にS3にアップロードして、Generative AI Usecases JPから利用する方法を説明します。

## 機能

- Wordドキュメントの作成・編集後、自動的にS3にアップロード
- 署名付きURL（期限付き）を返却
- AWS認証情報は環境変数またはIAMロールで管理

## 前提条件

- Python 3.11以上
- AWS アカウント
- S3バケット
- AWS認証情報（IAMロールまたはアクセスキー）

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env`ファイルを作成（`.env.example`を参考）：

```bash
S3_BUCKET_NAME=your-bucket-name
AWS_REGION=us-east-1
S3_URL_EXPIRATION=3600
```

AWS認証情報の設定（IAMロールを使用しない場合）：

```bash
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

### 3. S3バケットの準備

```bash
# バケット作成（既存の場合は不要）
aws s3 mb s3://your-bucket-name --region us-east-1

# バケットポリシーの設定（必要に応じて）
```

## Generative AI Usecases JPでの利用

### uvxを使用した設定

Generative AI Usecases JPの設定ファイルに以下を追加：

```json
{
  "mcpServers": {
    "word-document-server": {
      "command": "uvx",
      "args": ["--from", "office-word-mcp-server", "word_mcp_server"],
      "env": {
        "S3_BUCKET_NAME": "your-bucket-name",
        "AWS_REGION": "us-east-1",
        "S3_URL_EXPIRATION": "3600",
        "AWS_ACCESS_KEY_ID": "your-access-key",
        "AWS_SECRET_ACCESS_KEY": "your-secret-key"
      }
    }
  }
}
```

### IAMロールを使用する場合（推奨）

EC2やECSで実行する場合、IAMロールを使用することを推奨します：

```json
{
  "mcpServers": {
    "word-document-server": {
      "command": "uvx",
      "args": ["--from", "office-word-mcp-server", "word_mcp_server"],
      "env": {
        "S3_BUCKET_NAME": "your-bucket-name",
        "AWS_REGION": "us-east-1",
        "S3_URL_EXPIRATION": "3600"
      }
    }
  }
}
```

必要なIAMポリシー：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject"
      ],
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

## ローカル開発

### 1. パッケージのビルド

```bash
pip install build
python -m build
```

### 2. ローカルインストール

```bash
pip install -e .
```

### 3. 実行

```bash
word_mcp_server
```

## PyPIへの公開（オプション）

カスタムバージョンをPyPIに公開する場合：

```bash
# pyproject.tomlのバージョンを更新
# name = "office-word-mcp-server-s3" など

pip install twine
python -m build
twine upload dist/*
```

## 使用例

Generative AI Usecases JPでの使用例：

```
ユーザー: "report.docxという新しいドキュメントを作成して、タイトルを追加してください"

AI: [ドキュメントを作成]
結果:
Document report.docx created successfully
S3 URL: https://your-bucket-name.s3.amazonaws.com/report.docx?X-Amz-Algorithm=...
```

作成されたファイルは自動的にS3にアップロードされ、署名付きURLが返されます。

## トラブルシューティング

### S3アップロードが失敗する

- AWS認証情報が正しく設定されているか確認
- S3バケット名が正しいか確認
- IAMポリシーでS3へのアクセス権限があるか確認

### 環境変数が読み込まれない

- `.env`ファイルが正しい場所にあるか確認
- 環境変数名が正しいか確認（`S3_BUCKET_NAME`など）

### URLの有効期限

- デフォルトは3600秒（1時間）
- `S3_URL_EXPIRATION`環境変数で変更可能

## セキュリティ考慮事項

1. **認証情報の管理**
   - 本番環境ではIAMロールを使用
   - アクセスキーは環境変数で管理し、コードにハードコードしない

2. **S3バケットのアクセス制御**
   - 最小権限の原則に従う
   - 必要に応じてバケットポリシーを設定

3. **署名付きURLの有効期限**
   - 適切な有効期限を設定（デフォルト1時間）

## サポート

問題が発生した場合は、GitHubのIssuesで報告してください。
