from typing import List

from vizeval.core.interfaces import VizevalRepository
from vizeval.core.entities import Evaluation, User


class RepositoryService:
    def __init__(self, repository: VizevalRepository):
        self.repository = repository

    def get_evaluations_by_api_key(self, api_key: str) -> List[Evaluation]:
        """
        Retrieve all evaluations for a given API key.
        
        Args:
            api_key: The API key to fetch evaluations for
            
        Returns:
            List[Evaluation]: A list of evaluations associated with the API key's user
            
        Raises:
            ValueError: If the API key is invalid or no user is found
        """
        user = self.repository.get_user_from_api_key(api_key)
        
        if not user:
            raise ValueError("Invalid API key")
            
        return self.repository.list_evaluations(user_id=user.id)

    def add_user(self, user: User) -> str:
        """
        Add a new user and return its API key.
        
        Args:
            user: The user to add
            
        Returns:
            str: The API key of the added user
            
        Raises:
            ValueError: If the user already exists
        """
        return self.repository.add_user(user)

    def get_user_from_api_key(self, api_key: str) -> User:
        """
        Retrieve a user by their API key.
        
        Args:
            api_key: The API key to fetch the user for
            
        Returns:
            Optional[User]: The user associated with the API key, or None if not found
        """
        try:
            return self.repository.get_user_from_api_key(api_key)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))