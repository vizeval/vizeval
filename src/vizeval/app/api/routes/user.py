from fastapi import APIRouter, Depends, status
from typing import List

from vizeval.app.api.schemas.user import UserCreate, UserResponse
from vizeval.app.services.repository_service import RepositoryService
from vizeval.app.api.schemas.evaluation import Evaluation
from vizeval.core.entities import User as CoreUser
from vizeval.app.services.service_provider import get_repository_service

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    repository_service: RepositoryService = Depends(get_repository_service)
):
    """Create a new user and return their API key."""
    user_api_key = repository_service.add_user(CoreUser(name=user.name))
    return UserResponse(
        name=user.name,
        api_key=user_api_key,
    )

@router.get("/evaluations", response_model=List[Evaluation])
async def get_user_evaluations(
    api_key: str,
    repository_service: RepositoryService = Depends(get_repository_service)
):
    """Get all evaluations for a user by their API key."""
    core_evaluations = repository_service.get_evaluations_by_api_key(api_key)
    return [Evaluation.from_core(core_evaluation) for core_evaluation in core_evaluations]