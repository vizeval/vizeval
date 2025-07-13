from pydantic import BaseModel, Field
from typing import Dict, Optional, Any
from vizeval.core.entities import Evaluation as CoreEvaluation

class EvaluationRequest(BaseModel):
    system_prompt: str
    user_prompt: str
    response: str
    evaluator: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    api_key: str
    async_mode: bool = False

class EvaluationResponse(BaseModel):
    evaluator: str
    score: Optional[float] = None
    feedback: Optional[str] = None

class Evaluation(BaseModel):
    system_prompt: str
    user_prompt: str
    response: str
    user_id: str
    evaluator: str
    score: Optional[float] = None
    feedback: Optional[str] = None
    metadata: Dict[str, Any] = {}

    @classmethod
    def from_core(cls, core_evaluation: CoreEvaluation) -> "Evaluation":
        return cls(
            system_prompt=core_evaluation.system_prompt,
            user_prompt=core_evaluation.user_prompt,
            response=core_evaluation.response,
            user_id=core_evaluation.user_id,
            evaluator=core_evaluation.evaluator,
            score=core_evaluation.score,
            feedback=core_evaluation.feedback,
            metadata=core_evaluation.metadata
        )