from abc import ABC, abstractmethod
from typing import List, Optional

from vizeval.core.entities import Evaluation, User

class VizevalRepository(ABC):
    @abstractmethod
    def store_evaluation(self, evaluation: Evaluation) -> str:
        """Store an evaluation and return its ID"""
        pass

    @abstractmethod
    def get_evaluation(self, evaluation_id: str) -> Optional[Evaluation]:
        """Get an evaluation by ID"""
        pass

    @abstractmethod
    def list_evaluations(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Evaluation]:
        """List evaluations with pagination"""
        pass

    @abstractmethod
    def get_user_from_api_key(self, api_key: str) -> Optional[str]:
        """Get a user by API key"""
        pass
        
    @abstractmethod
    def add_user(self, user: User) -> str:
        """Add a new user and return its API key"""
        pass
        