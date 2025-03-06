from pydantic import BaseModel, EmailStr, Field


class SUserRegister(BaseModel):
    username: str = Field(..., title="Username", max_length=20)
    email: EmailStr = Field(..., title="Email")
    password: str = Field(..., title="Password")
    first_name: str = Field(..., title="First name", max_length=50)
    last_name: str = Field(..., title="Last name", max_length=50)

class SUserLogin(BaseModel):
    email: EmailStr = Field(..., title="Email")
    password: str = Field(..., title="Password")
