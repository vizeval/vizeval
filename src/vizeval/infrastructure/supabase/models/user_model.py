from pydantic import BaseModel


class UserModel(BaseModel):
    id: str
    name: str
    api_key: str
