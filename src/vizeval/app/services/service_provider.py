from fastapi import HTTPException, status

from vizeval.app.services.evaluation_service import EvaluationService
from vizeval.app.services.repository_service import RepositoryService

# These would typically be initialized in a dependency injection container
# For now, we'll use module-level variables
_repository = None
_queue = None

def initialize_services(repository, queue):
    """Initialize service dependencies."""
    global _repository, _queue
    _repository = repository
    _queue = queue

def get_evaluation_service() -> EvaluationService:
    """Get the evaluation service with initialized dependencies."""
    if not all([_repository, _queue]):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service dependencies not properly initialized"
        )
    
    return EvaluationService(
        repository=_repository,
        queue=_queue
    )

def get_repository_service() -> RepositoryService:
    """Get the repository service with initialized dependencies."""
    if not _repository:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Repository service not properly initialized"
        )
    return RepositoryService(_repository)
