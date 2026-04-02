import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import Base, SessionLocal, engine
from app.storage import upload_image


load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Jeligramy API")

allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

uploads_dir = Path(__file__).resolve().parent.parent / "uploads"
uploads_dir.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/posts", response_model=list[schemas.Post])
def list_posts(db: Session = Depends(get_db)) -> list[models.Post]:
    return db.query(models.Post).order_by(models.Post.created_at.desc()).all()


@app.post("/posts", response_model=schemas.Post)
async def create_post(
    file: UploadFile = File(...),
    caption: str = Form(default=""),
    db: Session = Depends(get_db),
) -> models.Post:
    if not (file.content_type or "").startswith("image/"):
        raise HTTPException(status_code=400, detail="画像ファイルを指定してください。")

    try:
        image_url = await upload_image(file)
    except Exception as exc:  # pragma: no cover
        raise HTTPException(
            status_code=500,
            detail=f"画像のアップロードに失敗しました: {exc}",
        ) from exc

    post = models.Post(image_url=image_url, caption=caption.strip() or None)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post
