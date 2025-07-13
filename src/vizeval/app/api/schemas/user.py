from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str = "mock-user-id"
    name: str = "mock-user"
    api_key: str = "mock-api-key"


class UserCreate(BaseModel):
    name: str = "mock-user"