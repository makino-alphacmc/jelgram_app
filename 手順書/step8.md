# Step 8: Fly.io へのデプロイ

## 📋 このステップでやること

Fly.io にデプロイして、誰でもアクセスできるようにします。

**推奨**: Fly.io（完全無料、クレジットカード不要、長期的に利用可能）

## ✅ 手順

### 1. 準備

#### 1-1. Fly.io アカウント作成

https://fly.io でアカウントを作成

#### 1-2. flyctl のインストール

```bash
# macOSの場合
brew install flyctl

# または、公式インストールスクリプトを使用
curl -L https://fly.io/install.sh | sh
```

#### 1-3. Fly.io にログイン

```bash
flyctl auth login
```

ブラウザが開いて、Fly.io アカウントでログインします。

### 2. API のデプロイ

#### 2-1. API ディレクトリに移動

```bash
cd insta-clone-api
```

#### 2-2. Fly.io アプリを初期化

```bash
flyctl launch
```

プロンプトに従って設定：

- **アプリ名**: `jeligramy-api`（または任意の名前）
- **リージョン**: `nrt`（東京）を選択
- **PostgreSQL**: 使用しない（SQLite を使用しているため）
- **Redis**: 使用しない

#### 2-3. fly.toml を編集

生成された `fly.toml` を編集：

```toml
app = "jeligramy-api"
primary_region = "nrt"

[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8000"

[[services]]
  internal_port = 8000
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

[[services.http_checks]]
  interval = "10s"
  timeout = "2s"
  grace_period = "5s"
  method = "GET"
  path = "/health"
```

#### 2-4. 環境変数を設定

```bash
# Supabase設定
flyctl secrets set SUPABASE_URL=https://xxxxx.supabase.co
flyctl secrets set SUPABASE_ANON_KEY=your_supabase_anon_key
flyctl secrets set SUPABASE_BUCKET=post-images

# CORS設定（後でフロントエンドのURLを設定）
flyctl secrets set ALLOWED_ORIGINS=https://jeligramy-front.fly.dev
```

#### 2-5. デプロイ

```bash
flyctl deploy
```

#### 2-6. アプリの URL を確認

```bash
flyctl status
```

API の URL は `https://jeligramy-api.fly.dev` のようになります。この URL をメモしておきます。

### 3. フロントエンドのデプロイ

#### 3-1. フロントエンドディレクトリに移動

```bash
cd ../insta-clone-front
```

#### 3-2. Fly.io アプリを初期化

```bash
flyctl launch
```

プロンプトに従って設定：

- **アプリ名**: `jeligramy-front`（または任意の名前）
- **リージョン**: `nrt`（東京）を選択
- **PostgreSQL**: 使用しない
- **Redis**: 使用しない

#### 3-3. fly.toml を編集

生成された `fly.toml` を編集：

```toml
app = "jeligramy-front"
primary_region = "nrt"

[build]
  dockerfile = "Dockerfile"
  build_args = [
    "NUXT_PUBLIC_API_BASE"
  ]

[[services]]
  internal_port = 80
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]
```

#### 3-4. 環境変数を設定

```bash
# APIのURLを設定（2-6で取得したURL）
flyctl secrets set NUXT_PUBLIC_API_BASE=https://jeligramy-api.fly.dev
```

#### 3-5. デプロイ（ビルド引数を渡す）

```bash
flyctl deploy --build-arg NUXT_PUBLIC_API_BASE=https://jeligramy-api.fly.dev
```

**注意**: `NUXT_PUBLIC_API_BASE` はビルド時に必要なので、`--build-arg` で渡します。

#### 3-6. アプリの URL を確認

```bash
flyctl status
```

フロントエンドの URL は `https://jeligramy-front.fly.dev` のようになります。

### 4. API の CORS 設定を更新

フロントエンドの URL が確定したら、API の CORS 設定を更新：

```bash
cd ../insta-clone-api
flyctl secrets set ALLOWED_ORIGINS=https://jeligramy-front.fly.dev
```

### 5. 動作確認

ブラウザで `https://jeligramy-front.fly.dev` にアクセスして、以下を確認：

- [ ] フロントエンドが表示される
- [ ] 投稿一覧が表示される
- [ ] 投稿機能が動作する
- [ ] 画像がアップロードされ、表示される

## 📝 重要な設定

### Dockerfile の確認

**フロントエンド（insta-clone-front/Dockerfile）**:

`NUXT_PUBLIC_API_BASE` をビルド引数として受け取れるようになっているか確認：

```dockerfile
ARG NUXT_PUBLIC_API_BASE=http://localhost:8000
ENV NUXT_PUBLIC_API_BASE=$NUXT_PUBLIC_API_BASE
```

（既に設定済み）

### 環境変数の設定場所

- **Fly.io の secrets**: `flyctl secrets set` で設定（本番環境用）
- **fly.toml の build_args**: ビルド時に渡す引数（フロントエンドの `NUXT_PUBLIC_API_BASE` など）

## ⚠️ 注意事項

- Fly.io は自動的に HTTPS を提供します（無料）
- アプリの URL は `https://アプリ名.fly.dev` の形式になります
- データベース（SQLite）は永続化されますが、アプリを再デプロイするとデータが消える可能性があります
- フロントエンドの `NUXT_PUBLIC_API_BASE` はビルド時に必要なので、`--build-arg` で渡す必要があります

## ✅ チェックリスト

- [ ] Fly.io アカウントを作成した
- [ ] `flyctl` をインストールした
- [ ] Fly.io にログインした
- [ ] API をデプロイした
- [ ] フロントエンドをデプロイした
- [ ] API の CORS 設定を更新した
- [ ] 動作確認が完了した

## 🔒 セキュリティチェックリスト

- [ ] `.env` ファイルが Git にコミットされていない（`.gitignore`に追加）
- [ ] Supabase のキーが適切に管理されている（Fly.io の secrets で設定）
- [ ] CORS 設定が適切（本番 URL のみ許可）

## 🎯 次のステップ

本番環境の準備が完了したら、**step9.md** に進んでください。
（リリース前チェック）
