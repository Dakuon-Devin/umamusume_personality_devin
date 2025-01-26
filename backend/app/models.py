from pydantic import BaseModel


# パスワードを除外したレスポンス用のモデル
class UserResponse(BaseModel):
    username: str
    full_name: str | None = None
    disabled: bool | None = None


# 性格診断クイズのリクエストデータ
class PersonalityQuizRequest(BaseModel):
    question1: str
    question2: str


# 性格診断クイズのレスポンスデータ
class PersonalityQuizResponse(BaseModel):
    name: str
    personality: str
    url: str
