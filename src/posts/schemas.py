from pydantic import BaseModel, Field


class SPost(BaseModel):
    title: str = Field(..., max_length=50)
    content: str = Field(..., max_length=500)
