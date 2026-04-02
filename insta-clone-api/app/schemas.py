from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Post(BaseModel):
    id: int
    image_url: str
    caption: str | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
