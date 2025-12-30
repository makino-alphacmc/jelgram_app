# Step 8: 本番環境へのデプロイ準備

## 📋 このステップでやること

本番環境で動作するように設定を調整し、デプロイの準備をします。

## ✅ 手順

### 8-1) 本番環境の選択

※ 目的: デプロイ先の前提を固め、以降の設定（ポート/ドメイン/SSL）を決めやすくする。

以下のいずれかを選択します：

- **VPS**（例: DigitalOcean, Linode, ConoHa）
- **クラウドサービス**（例: AWS, GCP, Azure）
- **自宅サーバー**
- **その他のサーバー**

**必要なもの**:

- Docker と Docker Compose がインストールされている
- ドメイン名（オプション、なくても IP アドレスでアクセス可能）

### 8-2) 本番用の環境変数設定

※ 目的: 本番固有のキーやオリジンを分離し、セキュアに設定する。

#### Backend（insta-clone-api/.env.production）

本番環境用の `.env.production` を作成します：

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your_production_anon_key
SUPABASE_BUCKET=post-images
ALLOWED_ORIGINS=https://your-domain.com,http://192.168.10.102:3000
```

**`ALLOWED_ORIGINS`の設定方法**:

`ALLOWED_ORIGINS`には、**フロントエンドアプリにアクセスする URL**を指定します。これは CORS（Cross-Origin Resource Sharing）の設定で、どのオリジンからのリクエストを許可するかを決めます。

**重要**: 指定するドメインや URL は、**実際にフロントエンドアプリが公開されている URL** である必要があります。適当なドメインを指定しても意味がありません。

**具体例**:

1. **ドメインを使用する場合**:

   ```env
   ALLOWED_ORIGINS=https://jeligramy.com,https://www.jeligramy.com
   ```

   - フロントエンドが `https://jeligramy.com` で公開されている場合
   - 複数のドメイン（www 付きなど）を許可する場合はカンマ区切り

2. **IP アドレスを使用する場合**:

   ```env
   ALLOWED_ORIGINS=http://192.168.10.102:3000
   ```

   - フロントエンドが `http://192.168.10.102:3000` で公開されている場合
   - IP アドレスは実際のサーバーの IP アドレスに置き換えてください（例: `ipconfig getifaddr en0` で確認）

3. **開発環境と本番環境の両方を許可する場合**:
   ```env
   ALLOWED_ORIGINS=http://localhost:3000,https://jeligramy.com
   ```
   - 開発中はローカル環境も許可したい場合

**ドメインの取得方法**:

ドメインは以下のいずれかの方法で取得・使用できます：

1. **有料ドメインサービス**:

   - 例: お名前.com、ムームードメイン、Google Domains など
   - 年間数百円〜数千円でドメインを取得
   - 取得後、DNS 設定でサーバーの IP アドレスと紐付け

2. **無料ドメインサービス**:

   - 例: Freenom（.tk, .ml, .ga など）、No-IP（動的 DNS）
   - 無料でドメインを取得可能（ただし制限あり）

3. **IP アドレスのみ使用**:
   - ドメインがなくても、IP アドレスとポート番号でアクセス可能
   - 例: `http://192.168.10.102:3000`
   - この場合は、`ALLOWED_ORIGINS=http://192.168.10.102:3000` と設定

**確認方法**:

フロントエンドの公開 URL は、以下の方法で確認できます：

**重要**: `localhost` はローカル開発環境専用です。本番環境では使用できません。

1. **ブラウザのアドレスバーを確認**:

   - **ローカル開発環境の場合**:

     - `http://localhost:3000` と表示される → これはローカル開発用
     - 本番環境では使用しない

   - **本番環境の場合**:
     - `http://192.168.10.102:3000` や `https://jeligramy.com` のように表示される
     - この URL を `ALLOWED_ORIGINS` に設定する

2. **サーバーの IP アドレスを確認**:

   **Linux の場合**:

   ```bash
   # サーバーに SSH で接続して実行
   hostname -I
   # または
   ip addr show
   # または
   curl ifconfig.me  # 外部IPアドレスを確認
   ```

   **macOS の場合**:

   ```bash
   # ローカルIPアドレス（Wi-Fiの場合）
   ipconfig getifaddr en0
   # または（有線の場合）
   ipconfig getifaddr en1
   # または（すべてのネットワークインターフェース）
   ifconfig | grep "inet " | grep -v 127.0.0.1
   # 外部IPアドレスを確認
   curl ifconfig.me
   ```

   **注意**:

   - `curl ifconfig.me` は外部 IP アドレス（インターネットから見た IP）を返しますが、IPv6 が返る場合があります
   - IPv4 の外部 IP アドレスを確認する場合は `curl -4 ifconfig.me` を使用してください
   - ローカルネットワーク内でアクセスする場合は、`ipconfig getifaddr en0` などで取得したローカル IP アドレス（`192.168.x.x`）を使用してください
   - **外部からアクセスする場合**: 外部 IP アドレスを使用し、ルーターのポートフォワーディング設定が必要です
   - **ローカルネットワーク内のみ**: ローカル IP アドレス（`192.168.x.x`）を使用します

3. **docker-compose.yml でポートマッピングを確認**:

   ```yaml
   front:
     ports:
       - '3000:80' # ホストの3000番ポート → コンテナの80番ポート
   ```

   - この場合、`http://サーバーのIPアドレス:3000` でアクセス可能

4. **実際にアクセスして確認**:
   - ブラウザで `http://サーバーのIPアドレス:3000` にアクセス
   - アプリが表示されれば、その URL が公開 URL

**設定例**:

- **ローカル開発環境**:

  - `http://localhost:3000` でアクセス → `ALLOWED_ORIGINS=http://localhost:3000` と設定（開発用）

- **本番環境（ローカルネットワーク内、IP アドレス使用）**:

  - サーバーの IP アドレスが `192.168.10.102` で、docker-compose.yml で `3000:80` とマッピングされている場合
  - ブラウザで `http://192.168.10.102:3000` にアクセスしてアプリが表示される
  - → `ALLOWED_ORIGINS=http://192.168.10.102:3000` と設定
  - **注意**: これは同じ Wi-Fi ネットワーク内のデバイスからのみアクセス可能です

  **実際の設定例（ローカルネットワーク内）**:

  ```env
  # insta-clone-api/.env.production
  SUPABASE_URL=https://xxxxx.supabase.co
  SUPABASE_ANON_KEY=your_production_anon_key
  SUPABASE_BUCKET=post-images
  ALLOWED_ORIGINS=http://192.168.10.102:3000
  ```

- **本番環境（外部ネットワーク、IPv4 アドレス使用）**:

  - 外部 IPv4 アドレスが `14.8.40.225` の場合（`curl -4 ifconfig.me` で確認）
  - ブラウザで `http://14.8.40.225:3000` にアクセスしてアプリが表示される
  - → `ALLOWED_ORIGINS=http://14.8.40.225:3000` と設定
  - **注意**: ルーターのポートフォワーディング設定が必要な場合があります
  - **推奨**: IPv4 アドレスの方が一般的に使いやすく、互換性が高いです

  **実際の設定例（外部ネットワーク、IPv4）**:

  ```env
  # insta-clone-api/.env.production
  SUPABASE_URL=https://xxxxx.supabase.co
  SUPABASE_ANON_KEY=your_production_anon_key
  SUPABASE_BUCKET=post-images
  ALLOWED_ORIGINS=http://14.8.40.225:3000
  ```

- **本番環境（外部ネットワーク、IPv6 アドレス使用）**:

  - 外部 IPv6 アドレスが `240b:12:28e1:2400:712a:763:e26c:1ac2` の場合（`curl ifconfig.me` で確認）
  - ブラウザで `http://[240b:12:28e1:2400:712a:763:e26c:1ac2]:3000` にアクセスしてアプリが表示される
  - → `ALLOWED_ORIGINS=http://[240b:12:28e1:2400:712a:763:e26c:1ac2]:3000` と設定
  - **注意**: IPv6 アドレスは角括弧 `[]` で囲む必要があります。ルーターやネットワークが IPv6 に対応している必要があります

  **実際の設定例（外部ネットワーク、IPv6）**:

  ```env
  # insta-clone-api/.env.production
  SUPABASE_URL=https://xxxxx.supabase.co
  SUPABASE_ANON_KEY=your_production_anon_key
  SUPABASE_BUCKET=post-images
  ALLOWED_ORIGINS=http://[240b:12:28e1:2400:712a:763:e26c:1ac2]:3000
  ```

- **本番環境（ドメイン使用）**:
  - ドメイン `jeligramy.com` を取得して設定した場合
  - ブラウザで `https://jeligramy.com` にアクセスしてアプリが表示される
  - → `ALLOWED_ORIGINS=https://jeligramy.com` と設定

**重要: ローカルネットワークと外部ネットワークの違い**:

- **ローカルネットワーク内（`192.168.x.x`など）**:

  - 同じ Wi-Fi ネットワーク内のデバイスからアクセス可能
  - 例: `http://192.168.10.102:3000` → 同じ Wi-Fi に接続しているデバイスからアクセス可能
  - 外部（インターネット）からはアクセス不可

- **外部ネットワーク（インターネット）**:
  - どのデバイスからでもアクセス可能（インターネット経由）
  - 外部 IP アドレス（パブリック IP）またはドメイン名が必要
  - 例: `http://14.8.40.225:3000`（IPv4）や `http://[240b:12:28e1:2400:712a:763:e26c:1ac2]:3000`（IPv6）や `https://jeligramy.com`
  - **注意**: 外部 IP アドレスを使用する場合、ルーターのポートフォワーディング設定が必要な場合があります
  - **推奨**: IPv4 アドレス（`14.8.40.225`など）の方が一般的に使いやすく、互換性が高いです

**外部 IP アドレスの確認方法**:

```bash
# IPv4の外部IPアドレスを確認
curl -4 ifconfig.me
# または
curl ipv4.icanhazip.com

# IPv6の外部IPアドレスを確認
curl -6 ifconfig.me
# または
curl ifconfig.me  # IPv6が返る場合があります
```

**IPv6 アドレスを使用する場合の注意**:

- IPv6 アドレスは角括弧 `[]` で囲む必要があります
- 例: `http://[240b:12:28e1:2400:712a:763:e26c:1ac2]:3000`
- ルーターやネットワークが IPv6 に対応している必要があります
- すべてのデバイスが IPv6 に対応しているとは限りません

**注意**:

- `localhost` は本番環境では使用できません。必ずサーバーの IP アドレスまたはドメイン名を使用してください
- `192.168.x.x` はローカルネットワーク内の IP アドレスです。同じネットワーク内のデバイスからアクセスする場合に使用します
- 外部ネットワークからアクセスする場合は、サーバーの外部 IP アドレスまたはドメイン名が必要です
- 外部 IP アドレスを使用する場合、ファイアウォールやルーターの設定でポート（3000, 8000）を開放する必要がある場合があります

**注意**:

- ドメインを指定する場合は、そのドメインで実際にアプリが公開されている必要があります
- ローカルネットワーク内（192.168.x.x など）と外部ネットワークでは IP アドレスが異なる場合があります

**注意**:

- `http://` と `https://` は区別されます（混在可能）
- ポート番号も含めて正確に指定してください
- 複数のオリジンを指定する場合はカンマ区切り（スペースなし）

#### Frontend（insta-clone-front/.env.production）

本番環境用の `.env.production` を作成します：

```env
NUXT_PUBLIC_API_BASE=https://your-api-domain.com
# または（ローカルネットワーク内、IPアドレス使用の場合）
NUXT_PUBLIC_API_BASE=http://192.168.10.102:8000
# または（外部ネットワーク、IPv4使用の場合）
NUXT_PUBLIC_API_BASE=http://14.8.40.225:8000
# または（外部ネットワーク、IPv6使用の場合）
NUXT_PUBLIC_API_BASE=http://[240b:12:28e1:2400:712a:763:e26c:1ac2]:8000
```

**実際の設定例**:

- **ローカルネットワーク内**:

  ```env
  # insta-clone-front/.env.production
  NUXT_PUBLIC_API_BASE=http://192.168.10.102:8000
  ```

- **外部ネットワーク（IPv4）**:

  ```env
  # insta-clone-front/.env.production
  NUXT_PUBLIC_API_BASE=http://14.8.40.225:8000
  ```

- **外部ネットワーク（IPv4）**:

  ```env
  # insta-clone-front/.env.production
  NUXT_PUBLIC_API_BASE=http://14.8.40.225:8000
  ```

- **外部ネットワーク（IPv6）**:
  ```env
  # insta-clone-front/.env.production
  NUXT_PUBLIC_API_BASE=http://[240b:12:28e1:2400:712a:763:e26c:1ac2]:8000
  ```

### 8-3) docker-compose.prod.yml の作成

※ 目的: 本番用リソース制限や env を明示し、デプロイをワンコマンド化する。

本番環境用の `docker-compose.prod.yml` を作成します：

```yaml
version: '3.8'

services:
  api:
    build:
      context: ./insta-clone-api
      dockerfile: Dockerfile
    container_name: insta-clone-api-prod
    ports:
      - '8000:8000'
    env_file:
      - ./insta-clone-api/.env.production
    volumes:
      - ./insta-clone-api/app.db:/app/app.db
      # ログを永続化する場合
      - ./insta-clone-api/logs:/app/logs
    restart: always
    # リソース制限（オプション）
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M

  front:
    build:
      context: ./insta-clone-front
      dockerfile: Dockerfile
      args:
        - NUXT_PUBLIC_API_BASE=${NUXT_PUBLIC_API_BASE}
    container_name: insta-clone-front-prod
    ports:
      - '3000:80'
    environment:
      - NUXT_PUBLIC_API_BASE=${NUXT_PUBLIC_API_BASE}
    depends_on:
      - api
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 256M
```

### 8-4) セキュリティ設定（オプション）

※ 目的: リバースプロキシで HTTPS やルーティングを制御し、安全に公開する。

#### Nginx リバースプロキシの設定（推奨）

本番環境では、Nginx をリバースプロキシとして使用することを推奨します：

```nginx
# /etc/nginx/sites-available/insta-clone
server {
    listen 80;
    server_name your-domain.com;

    # フロントエンド
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # バックエンドAPI
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 8-5) デプロイスクリプトの作成

※ 目的: pull→stop→build→up を自動化し、人的ミスを防ぐ。

`deploy.sh` を作成します：

```bash
#!/bin/bash

# デプロイスクリプト

echo "=== デプロイ開始 ==="

# 最新のコードを取得（Git使用の場合）
# git pull

# 既存のコンテナを停止
docker compose -f docker-compose.prod.yml down

# イメージをビルド
docker compose -f docker-compose.prod.yml build --no-cache

# コンテナを起動
docker compose -f docker-compose.prod.yml up -d

# ログを確認
docker compose -f docker-compose.prod.yml logs -f
```

実行権限を付与：

```bash
chmod +x deploy.sh
```

### 8-6) デプロイ手順

※ 目的: サーバーへの配置と起動の手順を定型化し、再現性を確保。

**デプロイ手順が必要な理由**:

現在、ローカル（自分の Mac）でアプリを動かしている場合、以下のような状況です：

- ✅ **開発・テストには問題なし**: `http://localhost:3000` で動作確認できる
- ❌ **24 時間 365 日稼働できない**: Mac を常時起動しておく必要がある
- ❌ **外部からアクセスしにくい**: 同じ Wi-Fi 内のデバイスからしかアクセスできない（`192.168.10.102`の場合）
- ❌ **本番環境として不安定**: PC を閉じたり、ネットワークが切れたりするとアクセスできなくなる

**リモートサーバーにデプロイするメリット**:

1. **24 時間 365 日稼働**: サーバーが常時起動しているため、いつでもアクセス可能
2. **外部からアクセス可能**: インターネット経由でどこからでもアクセスできる（ルーター設定が必要な場合あり）
3. **安定した運用**: サーバー専用の環境で、安定して動作する
4. **自分の PC を解放**: 開発用 PC を閉じても、アプリは動き続ける

**現在の状況での選択肢**:

- **ローカルで開発・テストのみ**: 現在のままで OK。リモートサーバーへのデプロイは不要
- **本番環境として公開したい**: 以下の 2 つの選択肢があります
  1. **リモートサーバー（VPS、クラウド）を使用**: サーバーを用意してデプロイ（`ssh user@your-server-ip`が必要）
  2. **自宅サーバー（現在の Mac）を使用**: ポートフォワーディング設定で外部からアクセス可能（`ssh user@your-server-ip`は不要）

**重要**: 現在、ローカル（自分の Mac）でアプリを動かしている場合、**リモートサーバーへのデプロイは不要**です。外部からアクセスしたい場合は、「8-7) 外部からアクセスできるようにする（自宅サーバーの場合）」の手順を参照してください。

**リモートサーバーへのデプロイ手順**:

#### リモートサーバーの情報を確認する方法

**`ssh user@your-server-ip`の意味**:

- **`user`**: サーバーのユーザー名（例: `ubuntu`, `root`, `admin`など）
- **`your-server-ip`**: サーバーのパブリック IP アドレス（外部からアクセス可能な IP）

**確認方法**:

1. **サーバーのパブリック IP アドレス（`your-server-ip`）**:

   **VPS やクラウドサービスの場合**:

   - サーバーの管理画面（ダッシュボード）で確認
   - 例: DigitalOcean、AWS、GCP、Azure などの管理画面
   - 通常、「IP Address」や「Public IP」として表示されます

   **自宅サーバーの場合**:

   ```bash
   # 外部IPアドレスを確認（IPv4）
   curl -4 ifconfig.me
   # または
   curl ipv4.icanhazip.com
   ```

   - 現在の外部 IP アドレス: `14.8.40.225`

2. **サーバーのユーザー名（`user`）**:

   **VPS やクラウドサービスの場合**:

   - サーバー作成時に指定したユーザー名
   - 一般的なユーザー名:
     - **Ubuntu/Debian**: `ubuntu`
     - **CentOS/RHEL**: `root` または `centos`
     - **Amazon Linux**: `ec2-user`
     - **その他**: サーバー作成時に指定したユーザー名

   **自宅サーバー（Mac）の場合**:

   ```bash
   # 現在のユーザー名を確認
   whoami
   # または
   echo $USER
   ```

   - 通常、Mac のユーザー名（例: `kimiko`）

**注意**:

- **リモートサーバー（VPS、クラウド）を使用する場合**: サーバーの管理画面で IP アドレスとユーザー名を確認してください
- **自宅サーバー（現在の Mac）を使用する場合**: `ssh user@your-server-ip`は不要です。直接 Mac で作業します

**リモートサーバーへの接続例**:

```bash
# VPSやクラウドサービスの場合（例）
ssh ubuntu@123.45.67.89
# または
ssh root@123.45.67.89

# 自宅サーバー（Mac）の場合
# SSH接続は不要。直接Macで作業します
```

1. **サーバーに接続**（リモートサーバーの場合のみ）:

```bash
ssh user@your-server-ip
# 例: ssh ubuntu@123.45.67.89
```

2. **プロジェクトをアップロード**:

```bash
# SCPでアップロード（例）
scp -r ~/work/insta-clone-* user@your-server-ip:/home/user/
scp docker-compose.prod.yml user@your-server-ip:/home/user/
```

または、Git リポジトリを使用：

```bash
git clone your-repo-url
cd insta-clone
```

3. **環境変数を設定**:

```bash
# .env.production ファイルを編集
nano insta-clone-api/.env.production
nano insta-clone-front/.env.production
```

4. **デプロイ実行**:

```bash
./deploy.sh
```

### 8-7) 外部からアクセスできるようにする（自宅サーバーの場合）

※ 目的: インターネット経由でどのデバイスからでもアクセスできるようにする。

**前提条件**:

- 現在、ローカル（自分の Mac）でアプリを動かしている
- 外部 IP アドレス: `14.8.40.225`（IPv4）
- ローカル IP アドレス: `192.168.10.102`

**必要な手順**:

#### 1. ルーターのポートフォワーディング設定

**ポートフォワーディングとは？**

ポートフォワーディングは、外部（インターネット）からのリクエストを、ルーター内の特定のデバイス（この場合は Mac）に転送する機能です。

**なぜ必要？**

- ルーターは外部と内部ネットワークの間にある「門番」のような役割をしています
- 外部から`http://14.8.40.225:3000`にアクセスしても、ルーターが「どのデバイスに転送すればいいか」分からないため、接続できません
- ポートフォワーディングを設定することで、「3000 番ポートへのアクセスは`192.168.10.102`（Mac）に転送する」とルーターに指示できます

**設定するポート**:

- **3000 番ポート**: フロントエンド用
- **8000 番ポート**: API 用

**設定方法**（ルーターの管理画面で設定）:

1. **ルーターの管理画面にアクセス**:

   - ブラウザで `http://192.168.1.1` または `http://192.168.0.1` にアクセス
   - ルーターの機種によって異なる場合があります（ルーターのマニュアルを確認）

2. **ログイン**:

   - ユーザー名とパスワードを入力（通常はルーターの裏面やマニュアルに記載）

3. **ポートフォワーディング設定画面を開く**:

   - 「ポートフォワーディング」「仮想サーバー」「NAT 設定」などのメニューを探す
   - ルーターの機種によって名称が異なります

4. **以下の設定を追加**:

   **設定 1: フロントエンド（3000 番ポート）**

   - **外部ポート（パブリックポート）**: `3000`
     - インターネットからアクセスする際のポート番号
   - **内部 IP（ローカル IP）**: `192.168.10.102`
     - Mac のローカル IP アドレス（`ipconfig getifaddr en0`で確認）
   - **内部ポート（プライベートポート）**: `3000`
     - Mac 上で動いているアプリのポート番号
   - **プロトコル**: `TCP`
     - HTTP/HTTPS は TCP プロトコルを使用

   **設定 2: API（8000 番ポート）**

   - **外部ポート**: `8000`
   - **内部 IP**: `192.168.10.102`
   - **内部ポート**: `8000`
   - **プロトコル**: `TCP`

**設定例（Buffalo ルーターの場合）**:

```
ポートマッピング設定
┌─────────────┬──────────────┬──────────────┬──────────┐
│ 外部ポート  │ 内部IP       │ 内部ポート   │ プロトコル│
├─────────────┼──────────────┼──────────────┼──────────┤
│ 3000        │ 192.168.10.102│ 3000        │ TCP      │
│ 8000        │ 192.168.10.102│ 8000        │ TCP      │
└─────────────┴──────────────┴──────────────┴──────────┘
```

**注意**:

- ルーターの機種によって設定方法が異なります
- ルーターのマニュアルを参照してください
- ファイアウォール設定も確認してください（ポートがブロックされていないか）
- 設定後、ルーターを再起動する必要がある場合があります

#### 2. 環境変数の設定

**重要: IP アドレスの使い分け**:

- **`192.168.10.102`**: ローカルネットワーク内（プライベート IP）

  - 同じ Wi-Fi 内のデバイスからのみアクセス可能
  - 外部（インターネット）からはアクセス不可

- **`14.8.40.225`**: 外部ネットワーク（パブリック IP）
  - どのデバイスからでもアクセス可能（インターネット経由）
  - ルーターのポートフォワーディング設定が必要

**用途に応じた設定**:

1. **ローカルネットワーク内のみで使用する場合**:

   - `NUXT_PUBLIC_API_BASE=http://192.168.10.102:8000`
   - 同じ Wi-Fi 内のデバイスからのみアクセス可能

2. **外部からもアクセスできるようにする場合**:
   - `NUXT_PUBLIC_API_BASE=http://14.8.40.225:8000`
   - どのデバイスからでもアクセス可能（ルーター設定が必要）

外部 IP アドレスを使用するように環境変数を設定します。

**Backend（insta-clone-api/.env）**:

`.env`ファイルを作成または編集します：

```bash
# insta-clone-api/.env を編集
nano insta-clone-api/.env
```

以下の内容を設定します：

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_BUCKET=post-images
ALLOWED_ORIGINS=http://14.8.40.225:3000,http://192.168.10.102:3000,http://localhost:3000
```

**注意**:

- ローカルネットワーク内（`192.168.10.102`）と外部ネットワーク（`14.8.40.225`）の両方からアクセスできるように、両方の IP アドレスを指定しています
- 開発用に`localhost`も追加しています

**Frontend（insta-clone-front/.env.production）**:

`.env.production`ファイルを作成または編集します：

```bash
# insta-clone-front/.env.production を編集
nano insta-clone-front/.env.production
```

**用途に応じた設定**:

1. **ローカルネットワーク内のみで使用する場合**:

   ```env
   NUXT_PUBLIC_API_BASE=http://192.168.10.102:8000
   ```

2. **外部からもアクセスできるようにする場合**:
   ```env
   NUXT_PUBLIC_API_BASE=http://14.8.40.225:8000
   ```

**注意**:

- 外部からアクセスする場合、フロントエンドから API にアクセスする際も外部 IP アドレス（`14.8.40.225:8000`）を使用する必要があります
- コンテナ間通信（`http://api:8000`）は、外部からアクセスする場合には使用できません
- **現在の設定**: `.env.production`に`NUXT_PUBLIC_API_BASE=http://192.168.10.102:8000`が設定されている場合、これはローカルネットワーク内でのみ動作します

#### 3. docker-compose.yml の更新

外部からアクセスする場合、`docker-compose.yml`の`front`サービスの環境変数を更新します：

**現在の設定（コンテナ間通信）**:

```yaml
front:
  environment:
    - NUXT_PUBLIC_API_BASE=http://api:8000
```

**外部アクセス用の設定**:

```yaml
front:
  environment:
    # 外部IPアドレスを使用（外部からアクセスする場合）
    - NUXT_PUBLIC_API_BASE=http://14.8.40.225:8000
```

**両方に対応する場合（推奨）**:

環境変数で切り替えられるようにする場合は、`.env`ファイルを作成して設定します：

```bash
# jeligramy/.env を作成
echo "NUXT_PUBLIC_API_BASE=http://14.8.40.225:8000" > .env
```

`docker-compose.yml`を以下のように更新：

```yaml
front:
  environment:
    # 環境変数から読み込む（外部アクセス用）
    - NUXT_PUBLIC_API_BASE=${NUXT_PUBLIC_API_BASE:-http://api:8000}
```

**注意**: `${NUXT_PUBLIC_API_BASE:-http://api:8000}`は、環境変数が設定されていない場合、デフォルトで`http://api:8000`（コンテナ間通信）を使用します。

#### 4. Docker Compose の再起動

設定を反映するために、Docker Compose を再起動します：

```bash
cd /Users/kimiko/Desktop/作業用/jeligramy
docker compose down
docker compose up -d --build
```

#### 5. 動作確認

**ローカルから確認**:

```bash
# ブラウザでアクセス
http://localhost:3000  # フロントエンド
http://localhost:8000/health  # API
```

**外部ネットワークから確認**:

- スマートフォンや他のデバイスから、Wi-Fi を**オフ**にして（モバイルデータ通信を使用）、以下の URL にアクセス：

```bash
http://14.8.40.225:3000  # フロントエンド
http://14.8.40.225:8000/health  # API
```

**注意**:

- 外部 IP アドレス（`14.8.40.225`）は、プロバイダーによって変わる場合があります（動的 IP の場合）
- 固定 IP アドレスが必要な場合は、プロバイダーに問い合わせてください
- セキュリティのため、本番環境では HTTPS の使用を推奨します

### 8-8) 動作確認

※ 目的: 本番でフロント/API/画像表示の一連の因果が成立するか検証する。

**ローカル環境での確認（現在の環境）**:

ローカルで開発・テストしている場合：

```bash
# ブラウザでアクセス
http://localhost:3000  # フロントエンド
http://localhost:8000  # API
```

**リモートサーバーにデプロイした場合の確認**:

リモートサーバーにデプロイした場合：

- [ ] `http://サーバーのIPアドレス:3000` でフロントエンドが表示される（例: `http://192.168.10.102:3000` または `http://14.8.40.225:3000`）
- [ ] `http://サーバーのIPアドレス:8000/health` で API が動作する（例: `http://192.168.10.102:8000/health` または `http://14.8.40.225:8000/health`）
- [ ] 投稿機能が動作する
- [ ] 画像がアップロードされ、表示される

## ✅ チェックリスト

- [ ] 本番環境のサーバーが準備された
- [ ] Docker と Docker Compose がインストールされた
- [ ] 本番用の環境変数が設定された
- [ ] `docker-compose.prod.yml` が作成された
- [ ] デプロイスクリプトが作成された
- [ ] サーバーにコードがアップロードされた
- [ ] 本番環境でアプリケーションが動作する

## 🔒 セキュリティチェックリスト

- [ ] `.env` ファイルが Git にコミットされていない（`.gitignore`に追加）
- [ ] Supabase のキーが適切に管理されている
- [ ] CORS 設定が適切（本番 URL のみ許可）
- [ ] ファイアウォール設定（必要に応じて）
- [ ] HTTPS の設定（ドメイン使用の場合）

## 🎯 次のステップ

本番環境の準備が完了したら、**step9.md** に進んでください。
（リリース前チェック）
