# Step 4: Backend セットアップ（FastAPI + SQLite + SQLAlchemy）

## 📋 このステップでやること

Instagram クローンのバックエンド API 環境を構築します。

- FastAPI プロジェクトの作成
- SQLite データベースの設定
- SQLAlchemy の設定
- 基本的なエンドポイントの実装

## ✅ 手順

### 4-1) プロジェクト作成

※ 目的: API 用の独立ディレクトリを切り、フロントと疎結合にする土台を作る（因果: 後の Docker 分離・デプロイが容易になる）。

```bash
# 作業ディレクトリに移動
cd ~/work

# バックエンドプロジェクト用のディレクトリを作成
mkdir insta-clone-api
cd insta-clone-api
```

### 4-2) 仮想環境の作成（推奨）

※ 目的: 依存衝突を避け、環境を再現可能にする。

```bash
# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
source venv/bin/activate  # macOS/Linux
# Windows の場合は: venv\Scripts\activate
```

### 4-3) 依存関係のインストール

※ 目的: FastAPI + SQLAlchemy を最小構成で動かす基盤を用意。

```bash
# FastAPI とその依存関係
pip install fastapi uvicorn[standard] python-dotenv

# SQLAlchemy（データベースORM）
pip install sqlalchemy
```

### 4-4) ディレクトリ構成の作成

※ 目的: app 配下に責務ごとにファイルを分け、保守性を確保。

```bash
# app ディレクトリと必要なファイルを作成
mkdir -p app
touch app/__init__.py
touch app/main.py
touch app/db.py
touch app/models.py
touch app/schemas.py
touch app/storage.py
```

### 4-5) データベース設定（app/db.py）

※ 目的: DB 接続と Session 管理を一元化し、各 API で再利用できるようにする。

`app/db.py` を編集します：

```python
from sqlalchemy import create_engine
# from sqlalchemy: SQLAlchemyライブラリから機能を読み込む
# create_engine: データベースへの接続を管理するエンジンを作成する関数

from sqlalchemy.ext.declarative import declarative_base
# declarative_base: データベースモデルの基底クラスを作成する関数

from sqlalchemy.orm import sessionmaker
# sessionmaker: データベースセッションを生成するファクトリー関数

# データベース接続URL（SQLite）
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
# SQLALCHEMY_DATABASE_URL: データベース接続のURL
# "sqlite:///./app.db": SQLiteデータベースファイルのパス
# sqlite:///: SQLiteの接続プロトコル
# ./app.db: 現在のディレクトリにapp.dbというファイルを作成

# データベースエンジンの作成（SQLite用の設定を含む）
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # SQLALCHEMY_DATABASE_URL: 接続先のデータベースURL
    connect_args={"check_same_thread": False}
    # connect_args: 接続時の追加引数
    # {"check_same_thread": False}: SQLite用の設定（マルチスレッド対応）
    # SQLiteはデフォルトでマルチスレッドを許可しないが、FastAPIは非同期で動作するため必要
)

# セッションファクトリーの作成（各リクエストでDBセッションを生成）
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# sessionmaker: セッションを生成するファクトリー関数
# autocommit=False: 自動コミットを無効化（明示的にcommit()を呼ぶ必要がある）
# autoflush=False: 自動フラッシュを無効化（クエリ実行時に自動保存しない）
# bind=engine: どのエンジンを使うかを指定

# データベースモデルの基底クラス
Base = declarative_base()
# declarative_base(): すべてのデータベースモデルの基底クラスを作成
# このBaseを継承することで、テーブル定義が簡単になる
```

### 4-6) データベースモデル（app/models.py）

※ 目的: posts テーブルの構造をコードで定義し、マイグレーション基盤に備える。

`app/models.py` を編集します：

```python
from sqlalchemy import Column, Integer, String, DateTime
# Column: データベースのカラム（列）を定義するクラス
# Integer: 整数型のデータ型
# String: 文字列型のデータ型
# DateTime: 日時型のデータ型

from sqlalchemy.sql import func
# func: SQL関数を使用するためのモジュール（例: func.now()で現在時刻を取得）

from app.db import Base
# Base: データベースモデルの基底クラス（app/db.pyで定義）

# 投稿データを表すデータベースモデル
class Post(Base):
    # class Post: 投稿データを表すクラス
    # (Base): Baseクラスを継承（テーブル定義が簡単になる）

    __tablename__ = "posts"
    # __tablename__: データベースに作成されるテーブル名を指定
    # "posts": テーブル名

    id = Column(Integer, primary_key=True, index=True)
    # Column: カラムを定義
    # Integer: 整数型
    # primary_key=True: 主キー（一意の識別子）に設定
    # index=True: インデックスを作成（検索が高速化される）

    image_url = Column(String, nullable=False)
    # String: 文字列型（長さ制限なし）
    # nullable=False: NULL値を許可しない（必須項目）

    caption = Column(String, nullable=True)
    # nullable=True: NULL値を許可（オプション項目、空でもOK）

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # DateTime(timezone=True): タイムゾーン情報を含む日時型
    # server_default=func.now(): データベース側で自動的に現在時刻を設定
    # func.now(): SQLのNOW()関数を実行（データベース側で現在時刻を取得）
```

### 4-7) スキーマ定義（app/schemas.py）

※ 目的: 入出力の型を明示し、バリデーションと自動ドキュメント化を行う。

`app/schemas.py` を編集します：

```python
from pydantic import BaseModel
# BaseModel: Pydanticの基底クラス（データバリデーションとシリアライゼーション用）
# FastAPIはPydanticを使って、リクエスト/レスポンスの型チェックとバリデーションを行う

from datetime import datetime
# datetime: 日時を扱うためのクラス

# 投稿データの基本スキーマ（共通フィールド）
class PostBase(BaseModel):
    # class PostBase: 投稿データの基本スキーマ（共通フィールドを定義）
    # (BaseModel): PydanticのBaseModelを継承

    image_url: str
    # image_url: 画像URL（文字列型、必須項目）
    # str: 文字列型

    caption: str | None = None
    # caption: キャプション（文字列型またはNone、オプション）
    # str | None: Python 3.10+の記法で、strまたはNoneを意味
    # = None: デフォルト値をNoneに設定（指定しなくてもOK）

# 新規投稿作成時のリクエストスキーマ
class PostCreate(PostBase):
    # class PostCreate: 新規投稿作成時のリクエストスキーマ
    # (PostBase): PostBaseを継承（image_urlとcaptionを含む）
    pass
    # pass: 何も追加しない（PostBaseのフィールドをそのまま使用）
    # idやcreated_atは含まない（これらは自動生成されるため）

# 投稿データのレスポンススキーマ（全フィールドを含む）
class Post(PostBase):
    # class Post: 投稿データのレスポンススキーマ（全フィールドを含む）
    # (PostBase): PostBaseを継承

    id: int
    # id: 投稿ID（整数型、データベースで自動生成）

    created_at: datetime
    # created_at: 作成日時（datetime型、データベースで自動設定）

    class Config:
        # class Config: Pydanticの設定クラス
        from_attributes = True
        # from_attributes = True: SQLAlchemyモデルから自動的にPydanticモデルに変換可能
        # これにより、db.query(Post).all()で取得したデータを、そのままPostスキーマとして返せる
```

### 4-8) メインアプリケーション（app/main.py）

※ 目的: CORS やヘルスチェックを含む最小 API を構築し、動作確認の基準点を作る。

`app/main.py` を編集します：

```python
from fastapi import FastAPI, Depends, HTTPException
# FastAPI: FastAPIアプリケーションのクラス
# Depends: 依存性注入（各エンドポイントでDBセッションなどを取得）
# HTTPException: HTTPエラーレスポンスを返すための例外クラス

from fastapi.middleware.cors import CORSMiddleware
# CORSMiddleware: CORS（Cross-Origin Resource Sharing）設定用のミドルウェア
# 異なるオリジン（プロトコル・ドメイン・ポート）間での通信を許可

from sqlalchemy.orm import Session
# Session: データベースセッションの型

from typing import List
# List: リスト（配列）の型ヒント

import os
# os: オペレーティングシステム関連の機能（環境変数の取得など）

from dotenv import load_dotenv
# load_dotenv: .envファイルから環境変数を読み込む関数

from app import models, schemas
# models: データベースモデル（app/models.py）
# schemas: Pydanticスキーマ（app/schemas.py）

from app.db import SessionLocal, engine
# SessionLocal: データベースセッションを生成するファクトリー
# engine: データベースエンジン

# 環境変数の読み込み
load_dotenv()
# load_dotenv(): .envファイルから環境変数を読み込む
# これにより、os.getenv()で環境変数にアクセスできる

# データベーステーブルの自動作成
models.Base.metadata.create_all(bind=engine)
# models.Base.metadata: すべてのモデルのメタデータ（テーブル定義情報）
# create_all(): テーブルを自動作成
# bind=engine: どのエンジンを使うかを指定

# FastAPIアプリケーションのインスタンス作成
app = FastAPI()
# FastAPI(): FastAPIアプリケーションのインスタンスを作成
# app: APIのエントリーポイント（エンドポイントを追加していく）

# CORS設定（フロントエンドからのアクセスを許可）
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
# os.getenv(): 環境変数を取得
# "ALLOWED_ORIGINS": 環境変数のキー
# "http://localhost:3000": デフォルト値（環境変数が存在しない場合）
# .split(","): カンマで分割してリストに変換（複数のオリジンを指定可能）

app.add_middleware(
    # add_middleware(): ミドルウェアを追加（リクエスト/レスポンスを処理する前後に実行）
    CORSMiddleware,
    # CORSMiddleware: CORS設定用のミドルウェア
    allow_origins=allowed_origins,
    # allow_origins: 許可するオリジンのリスト
    allow_credentials=True,
    # allow_credentials: クッキーなどの認証情報を許可
    allow_methods=["*"],
    # allow_methods: 許可するHTTPメソッド（["*"]はすべてのメソッドを許可）
    allow_headers=["*"],
    # allow_headers: 許可するHTTPヘッダー（["*"]はすべてのヘッダーを許可）
)

# データベースセッションの依存関係（各エンドポイントでDBセッションを取得）
def get_db():
    # get_db: データベースセッションを取得する関数（依存性注入で使用）
    db = SessionLocal()
    # SessionLocal(): 新しいデータベースセッションを作成
    try:
        # try: エラーが発生する可能性のある処理を囲む
        yield db
        # yield: ジェネレータ関数（値を返して処理を一時停止）
        # db: セッションを呼び出し元（エンドポイント）に渡す
    finally:
        # finally: 成功・失敗に関わらず必ず実行される処理
        db.close()
        # db.close(): セッションを閉じる（メモリリークを防ぐ）

# ヘルスチェックエンドポイント
@app.get("/health")
# @app.get: GETリクエストを受け付けるエンドポイントを定義（デコレータ）
# "/health": エンドポイントのパス

def health_check():
    # health_check: ヘルスチェック用の関数
    return {"status": "ok"}
    # return: レスポンスを返す
    # {"status": "ok"}: 辞書形式のデータ（FastAPIが自動的にJSONに変換）

# 投稿一覧取得エンドポイント
@app.get("/posts", response_model=List[schemas.Post])
# "/posts": エンドポイントのパス
# response_model: レスポンスの型を指定（自動ドキュメント生成に使用）
# List[schemas.Post]: 投稿のリストを返す

def get_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # get_posts: 投稿一覧を取得する関数
    # skip: int = 0: スキップする件数（デフォルト値は0、ページネーション用）
    # limit: int = 100: 取得する最大件数（デフォルト値は100）
    # db: Session = Depends(get_db): データベースセッション（依存性注入）
    # Depends(get_db): get_db関数を実行してセッションを取得

    # データベースから投稿を取得（作成日時の降順でソート）
    posts = db.query(models.Post).order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()
    # db.query(models.Post): Postモデルをクエリ（SQLのSELECT文を生成）
    # .order_by(): ソート順を指定
    # models.Post.created_at.desc(): 作成日時の降順（新しい順）
    # .offset(skip): スキップする件数（SQLのOFFSET句）
    # .limit(limit): 取得する最大件数（SQLのLIMIT句）
    # .all(): クエリを実行して結果をリストとして取得

    return posts
    # return: 取得した投稿リストを返す（FastAPIが自動的にJSONに変換）

# 投稿作成エンドポイント（画像アップロード機能はStep 5で実装）
@app.post("/posts", response_model=schemas.Post)
# @app.post: POSTリクエストを受け付けるエンドポイントを定義
# response_model=schemas.Post: レスポンスの型を指定

def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # create_post: 新規投稿を作成する関数
    # post: schemas.PostCreate: リクエストボディ（FastAPIが自動的にPydanticモデルに変換）

    # PydanticモデルからSQLAlchemyモデルに変換
    db_post = models.Post(**post.dict())
    # post.dict(): Pydanticモデルを辞書に変換
    # **post.dict(): 辞書を展開してキーワード引数として渡す
    # models.Post(): Postモデルのインスタンスを作成

    # セッションに追加
    db.add(db_post)
    # db.add(): セッションに追加（まだデータベースには保存されていない）

    # データベースにコミット
    db.commit()
    # db.commit(): 変更をデータベースに永続化（SQLを実行）

    # オブジェクトをリフレッシュ（自動生成されたidやcreated_atを取得）
    db.refresh(db_post)
    # db.refresh(): データベースから最新データを取得（idやcreated_atが設定される）

    return db_post
    # return: 作成された投稿データを返す（FastAPIが自動的にJSONに変換）
```

### 4-9) 環境変数ファイル（.env）

※ 目的: 環境依存値をコードから分離し、本番/開発を切り替えやすくする。

`.env` ファイルを作成します：

```bash
cat > .env << 'EOF'
ALLOWED_ORIGINS=http://localhost:3000
EOF
```

### 4-10) ローカル起動と動作確認

※ 目的: /health と /docs が通ることを確認し、以降の機能追加の足場にする（因果: ここで失敗を潰すと後続デバッグが楽）。

```bash
# 仮想環境が有効化されていることを確認
# （プロンプトに (venv) が表示されているはず）

# サーバーを起動
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

ブラウザで以下を確認：

- `http://localhost:8000/health` → `{"status": "ok"}` が表示される
- `http://localhost:8000/docs` → Swagger UI が表示される

## ✅ チェックリスト

- [ ✅ ] FastAPI プロジェクトが作成された
- [ ✅ ] 仮想環境が作成され、有効化された
- [ ✅ ] 必要なパッケージがインストールされた
- [ ✅ ] `app/db.py` でデータベース接続が設定された
- [ ✅ ] `app/models.py` で Post モデルが定義された
- [ ✅ ] `app/schemas.py` で Pydantic スキーマが定義された
- [ ✅ ] `app/main.py` で基本的なエンドポイントが実装された
- [ ✅ ] `/health` エンドポイントが動作する
- [ ✅ ] `/docs` で Swagger UI が表示される

## 🎯 次のステップ

バックエンドの基本設定が完了したら、**step5.md** に進んでください。
（画像保存：Supabase Storage の設定）
