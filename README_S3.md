# Office-Word-MCP-Server with S3 Upload

このバージョンは、元の[Office-Word-MCP-Server](https://github.com/GongRzhe/Office-Word-MCP-Server)にS3自動アップロード機能を追加したものです。

## 追加機能

- ✅ Wordドキュメント作成・編集後に自動的にS3にアップロード
- ✅ 署名付きURL（期限付き）を自動生成
- ✅ AWS IAMロール対応
- ✅ Generative AI Usecases JP対応

## クイックスタート

### 1. インストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数設定

```bash
export S3_BUCKET_NAME=your-bucket-name
export AWS_REGION=us-east-1
export S3_URL_EXPIRATION=3600
```

### 3. 実行

```bash
python word_mcp_server.py
```

## Generative AI Usecases JPでの使用

設定ファイルに以下を追加：

```json
{
  "mcpServers": {
    "word-document-server": {
      "command": "uvx",
      "args": ["--from", "office-word-mcp-server", "word_mcp_server"],
      "env": {
        "S3_BUCKET_NAME": "your-bucket-name",
        "AWS_REGION": "us-east-1"
      }
    }
  }
}
```

詳細は[AWS_DEPLOYMENT.md](./AWS_DEPLOYMENT.md)を参照してください。

## 変更点

### 新規ファイル
- `word_document_server/utils/s3_uploader.py` - S3アップロード機能
- `.env.example` - 環境変数テンプレート
- `AWS_DEPLOYMENT.md` - デプロイガイド

### 更新ファイル
- `requirements.txt` - boto3追加
- `pyproject.toml` - boto3依存関係追加
- `word_document_server/tools/document_tools.py` - S3アップロード統合
- `word_document_server/tools/content_tools.py` - S3アップロード統合
- `word_document_server/tools/format_tools.py` - S3アップロード統合

## 動作

全てのドキュメント作成・更新操作後、自動的に：

1. ファイルをS3にアップロード
2. 署名付きURLを生成（デフォルト1時間有効）
3. レスポンスにURLを含めて返却

例：
```
Document report.docx created successfully
S3 URL: https://your-bucket-name.s3.amazonaws.com/report.docx?X-Amz-Algorithm=...
```

## 環境変数

| 変数名 | 必須 | デフォルト | 説明 |
|--------|------|-----------|------|
| S3_BUCKET_NAME | ✅ | - | S3バケット名 |
| AWS_REGION | ❌ | us-east-1 | AWSリージョン |
| S3_URL_EXPIRATION | ❌ | 3600 | URL有効期限（秒） |
| AWS_ACCESS_KEY_ID | ❌ | - | AWSアクセスキー（IAMロール使用時は不要） |
| AWS_SECRET_ACCESS_KEY | ❌ | - | AWSシークレットキー（IAMロール使用時は不要） |

## ライセンス

MIT License - 元のプロジェクトと同じ
