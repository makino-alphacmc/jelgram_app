# Jeligramy

## 概要

Instagram 風の投稿アプリケーションです。画像とキャプションを投稿し、タイムラインで一覧表示できます。

## 機能

- **投稿一覧表示**: タイムラインで投稿を一覧表示
- **新規投稿**: 画像とキャプションを投稿

## 技術スタック

- **Frontend**: Nuxt 3, Vue 3, Nuxt UI
- **Backend API**: FastAPI, SQLAlchemy
- **Database**: SQLite
- **Storage**: Supabase Storage またはローカル保存
- **Infrastructure**: Docker, Docker Compose

## セットアップ

### 前提条件

- Docker と Docker Compose がインストールされていること
- Supabase は任意です。未設定でも開発環境ではローカル保存で動きます

### 環境変数の設定

`insta-clone-api/.env`:

```env
SUPABASE_URL=your-supabase-url-here
SUPABASE_ANON_KEY=your-supabase-anon-key-here
SUPABASE_BUCKET=post-images
ALLOWED_ORIGINS=http://localhost:3000
APP_BASE_URL=http://localhost:8000
```

`insta-clone-front/.env`:

```env
NUXT_PUBLIC_API_BASE=http://localhost:8000
```

### 起動方法

```bash
# 開発用コンテナをビルドして起動
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
- **Swagger UI**: http://localhost:8000/docs

## 実装済み

- タイムライン画面
- 新規投稿画面
- `GET /health`
- `GET /posts`
- `POST /posts`
- 画像のローカル保存フォールバック

---

※ UI は `仕様書/MVP/モック画面` を基準にしています。
