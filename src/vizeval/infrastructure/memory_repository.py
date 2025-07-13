from typing import List, Optional, Dict
import uuid

from vizeval.core.interfaces.vizeval_repository import VizevalRepository
from vizeval.core.entities import User, Evaluation


class MemoryRepository(VizevalRepository):
    def __init__(self):
        self.users = {}  # api_key -> User
        self.evaluations = {}  # id -> Evaluation
        self.user_evaluations = {}  # user_id -> List[evaluation_id]
    
    def store_evaluation(self, evaluation: Evaluation) -> str:
        """Store an evaluation and return its ID"""
        if not hasattr(evaluation, 'id') or not evaluation.id:
            evaluation.id = str(uuid.uuid4())
        
        self.evaluations[evaluation.id] = evaluation
        
        if evaluation.user_id and evaluation.user_id in self.user_evaluations:
            self.user_evaluations[evaluation.user_id].append(evaluation.id)
        
        return evaluation.id
    
    def get_evaluation(self, evaluation_id: str) -> Optional[Evaluation]:
        """Get an evaluation by ID"""
        return self.evaluations.get(evaluation_id)
    
    def list_evaluations(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Evaluation]:
        """List evaluations with pagination"""
        evaluation_ids = self.user_evaluations.get(user_id, [])
        paginated_ids = evaluation_ids[offset:offset + limit]
        return [self.evaluations[eval_id] for eval_id in paginated_ids if eval_id in self.evaluations]
    
    def get_user_from_api_key(self, api_key: str) -> Optional[User]:
        """Get a user by API key"""
        return self.users.get(api_key)
    
    def add_user(self, user: User) -> str:
        """Add a new user and return its API key"""
        if not user.api_key:
            user.api_key = str(uuid.uuid4())
        
        self.users[user.api_key] = user
        self.user_evaluations[user.id] = []
        
        return user.api_key
