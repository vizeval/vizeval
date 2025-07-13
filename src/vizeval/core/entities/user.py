from dataclasses import dataclass
from uuid import uuid4

@dataclass
class User:
    name: str
    api_key: str = "mock-api-key"
    id: str = "mock-user-id"
