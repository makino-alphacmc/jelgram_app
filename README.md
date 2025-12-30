# Jeligramy

## 概要

Instagram 風の投稿アプリケーションです。画像とキャプションを投稿し、タイムラインで一覧表示できます。

## 機能

- **投稿一覧表示**: タイムラインで投稿を一覧表示
- **新規投稿**: 画像とキャプションを投稿

## 技術スタック

- **Frontend**: Nuxt 4, Vue 3, Tailwind CSS, shadcn-nuxt
- **Backend API**: FastAPI, SQLAlchemy
- **Database**: SQLite
- **Storage**: Supabase Storage
- **Infrastructure**: Docker, Docker Compose

## セットアップ

### 前提条件

- Docker と Docker Compose がインストールされていること
- Supabase アカウント（画像ストレージ用）

### 環境変数の設定

`insta-clone-api/.env` ファイルを作成し、以下の環境変数を設定してください：

```env
SUPABASE_URL=your-supabase-url-here
SUPABASE_ANON_KEY=your-supabase-anon-key-here
SUPABASE_BUCKET=post-images
ALLOWED_ORIGINS=http://localhost:3000
```

### 起動方法

```bash
# コンテナをビルドして起動
docker compose up -d --build

# ログを確認
docker compose logs -f

# 停止
docker compose down
```

### アクセス

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API ヘルスチェック**: http://localhost:8000/health

## 今後の予定

- ユーザー登録
- ログイン機能
- 削除・更新機能の追加

---

※ 本プロジェクトは学習およびプロトタイプ開発を目的としています。
※ フロントと API を分離することで、将来的な UI 変更や機能拡張に対応しやすい構成としています。
