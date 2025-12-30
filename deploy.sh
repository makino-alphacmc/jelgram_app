# デプロイスクリプト

echo "=== デプロイ開始 ==="

# 最新のコードを取得（Git使用の場合）
git pull

# .env.productionからNUXT_PUBLIC_API_BASEを読み込む
if [ -f insta-clone-front/.env.production ]; then
    export NUXT_PUBLIC_API_BASE=$(grep NUXT_PUBLIC_API_BASE insta-clone-front/.env.production | cut -d'=' -f2)
    echo "NUXT_PUBLIC_API_BASE=$NUXT_PUBLIC_API_BASE"
fi

# 既存のコンテナを停止
docker compose -f docker-compose.prod.yml down

# イメージをビルド
docker compose -f docker-compose.prod.yml build --no-cache

# コンテナを起動
docker compose -f docker-compose.prod.yml up -d

# ログを確認
docker compose -f docker-compose.prod.yml logs -f