from pydantic import BaseModel, EmailStr


class SUserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class SUserLogin(BaseModel):
    email: EmailStr
    password: str
