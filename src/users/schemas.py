from pydantic import BaseModel, EmailStr


class SUserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
