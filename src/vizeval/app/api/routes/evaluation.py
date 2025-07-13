from fastapi import APIRouter, Depends, HTTPException, status

from vizeval.app.api.schemas.evaluation import (
    EvaluationRequest, 
    EvaluationResponse,
)
from vizeval.core.entities import EvaluationRequest as CoreEvaluationRequest
from vizeval.app.services.evaluation_service import EvaluationService

router = APIRouter(prefix="/evaluation", tags=["evaluation"])

# These would typically be initialized in a dependency injection container
# For now, we'll use module-level variables
_repository = None  # Should be an instance of VizevalRepository
_queue = None  # Should be an instance of EvaluationQueue

def get_evaluation_service() -> EvaluationService:
    if not all([_repository, _queue]):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service dependencies not properly initialized"
        )
    
    return EvaluationService(
        repository=_repository,
        queue=_queue
    )


@router.post("/", response_model=EvaluationResponse, status_code=status.HTTP_201_CREATED)
async def create_evaluation(
    request: EvaluationRequest,
    evaluation_service: EvaluationService = Depends(get_evaluation_service)
):
    """Create a new evaluation.
    
    If async_evaluation is True, queues the evaluation and returns a status response.
    If async_evaluation is False, performs the evaluation synchronously and returns the evaluation score and feedback.
    """
    core_request = CoreEvaluationRequest(
        system_prompt=request.system_prompt,
        user_prompt=request.user_prompt,
        model_response=request.response,
        evaluator_name=request.evaluator,
        metadata=request.metadata,
        api_key=request.api_key
    )
    
    if request.async_mode:
        result = evaluation_service.evaluate_async(core_request)
        return EvaluationResponse(
            evaluator=core_request.evaluator_name,
            score=result.score,
            feedback=result.feedback
        )
    
    result = evaluation_service.evaluate_sync(core_request)
    
    return EvaluationResponse(
        evaluator=core_request.evaluator_name,
        score=result.score,
        feedback=result.feedback
    )