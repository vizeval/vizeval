from typing import Dict, Any, Optional
from pydantic import BaseModel


class EvaluationModel(BaseModel):
    id: str
    system_prompt: str
    user_prompt: str
    response: str
    user_id: str
    evaluator: str
    score: Optional[float] = None
    feedback: Optional[str] = None
    metadata: Dict[str, Any] = {}
