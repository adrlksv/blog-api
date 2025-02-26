from pydantic import BaseModel


class SPost(BaseModel):
    title: str 
    content: str
