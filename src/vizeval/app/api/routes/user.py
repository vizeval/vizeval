from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from vizeval.app.api.schemas.user import UserCreate, UserResponse
from vizeval.app.services.repository_service import RepositoryService
from vizeval.app.api.schemas.evaluation import Evaluation
from vizeval.core.entities import Evaluation as CoreEvaluation
from vizeval.core.entities import User as CoreUser

router = APIRouter(prefix="/user", tags=["user"])

_repository = None  # Should be an instance of VizevalRepository

def get_repository_service() -> RepositoryService:
    if not _repository:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Repository service not properly initialized"
        )
    return RepositoryService(_repository)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    repository_service: RepositoryService = Depends(get_repository_service)
):
    """Create a new user and return their API key."""
    created_user = repository_service.add_user(CoreUser(name=user.name))
    return UserResponse(
        name=created_user.name,
        api_key=created_user.api_key,
    )

@router.get("/evaluations", response_model=List[Evaluation])
async def get_user_evaluations(
    api_key: str,
    repository_service: RepositoryService = Depends(get_repository_service)
):
    """Get all evaluations for a user by their API key."""
    core_evaluations = repository_service.get_evaluations_by_api_key(api_key)
    return [Evaluation.from_core(core_evaluation) for core_evaluation in core_evaluations]