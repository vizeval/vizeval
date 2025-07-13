from fastapi import APIRouter, Depends, status

from vizeval.app.api.schemas.evaluation import (
    EvaluationRequest, 
    EvaluationResponse,
)
from vizeval.core.entities import EvaluationRequest as CoreEvaluationRequest
from vizeval.app.services.evaluation_service import EvaluationService
from vizeval.app.services.service_provider import get_evaluation_service

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


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
        response=request.response,
        evaluator=request.evaluator,
        metadata=request.metadata,
        async_mode=request.async_mode
    )
    
    if request.async_mode:
        result = evaluation_service.evaluate_async(core_request)
        return EvaluationResponse(
            evaluator=core_request.evaluator,
            score=result.score,
            feedback=result.feedback
        )
    
    result = evaluation_service.evaluate_sync(core_request)
    
    return EvaluationResponse(
        evaluator=core_request.evaluator,
        score=result.score,
        feedback=result.feedback
    )