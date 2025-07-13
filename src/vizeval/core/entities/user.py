from dataclasses import dataclass
from uuid import uuid4

@dataclass
class User:
    name: str
    api_key: str = str(uuid4())
    id: str = str(uuid4())
