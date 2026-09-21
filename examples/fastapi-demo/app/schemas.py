from pydantic import BaseModel, Field


class LinkCreate(BaseModel):
    phone: str = Field(min_length=1)
    message: str = ""
    custom_slug: str | None = Field(default=None, min_length=3, max_length=32)
