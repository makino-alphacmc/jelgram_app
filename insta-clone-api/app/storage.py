import os
import uuid
from pathlib import Path

from fastapi import UploadFile

try:
    from supabase import Client, create_client
except Exception:  # pragma: no cover
    Client = None
    create_client = None


BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _get_supabase() -> tuple[Client | None, str | None]:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    bucket = os.getenv("SUPABASE_BUCKET", "post-images")
    if not url or not key or create_client is None:
        return None, None
    return create_client(url, key), bucket


async def upload_image(file: UploadFile) -> str:
    extension = Path(file.filename or "image.jpg").suffix or ".jpg"
    filename = f"{uuid.uuid4().hex}{extension.lower()}"
    content = await file.read()

    supabase, bucket = _get_supabase()
    if supabase and bucket:
        supabase.storage.from_(bucket).upload(
            filename,
            content,
            file_options={"content-type": file.content_type or "image/jpeg"},
        )
        return supabase.storage.from_(bucket).get_public_url(filename)

    output = UPLOAD_DIR / filename
    output.write_bytes(content)

    base_url = os.getenv("APP_BASE_URL", "http://localhost:8000").rstrip("/")
    return f"{base_url}/uploads/{filename}"
