from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ResetPasswordRequest(BaseModel):
    new_password: str
    token: str

class VerifyResetTokenRequest(BaseModel):
    token: str

class ChangePasswordRequest(BaseModel):
    new_password: str
    old_password: str
