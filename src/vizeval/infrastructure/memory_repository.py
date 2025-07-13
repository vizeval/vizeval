from typing import Dict, List, Optional, Any
import uuid

from vizeval.core.interfaces.vizeval_repository import VizevalRepository
from vizeval.core.entities import Evaluation, User


class MemoryRepository(VizevalRepository):
    def __init__(self):
        self.evaluations: Dict[str, Evaluation] = {}
        self.users: Dict[str, User] = {}
        self.api_keys: Dict[str, str] = {}
    
    def store_evaluation(self, evaluation: Evaluation) -> str:
        evaluation_id = str(uuid.uuid4())
        self.evaluations[evaluation_id] = evaluation
        return evaluation_id
    
    def list_evaluations(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Evaluation]:
        user_evaluations = [eval for eval in self.evaluations.values() if eval.user_id == user_id]
        return user_evaluations[offset:offset + limit]
    
    def get_user_from_api_key(self, api_key: str) -> Optional[User]:
        user_id = self.api_keys.get(api_key)
        return self.users.get(user_id)
    
    def add_user(self, user: User) -> str:
        user_id = "mock-user-id"
        api_key = "mock-api-key"
        
        user.id = user_id
        user.api_key = api_key
        
        self.users[user_id] = user
        self.api_keys[api_key] = user_id
        
        return api_key
