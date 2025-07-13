from dataclasses import dataclass   
from typing import Optional, Dict, Any


@dataclass
class Evaluation:
    system_prompt: str
    user_prompt: str
    response: str
    user_id: str
    evaluator: str
    score: Optional[float] = None
    feedback: Optional[str] = None
    metadata: Dict[str, Any] = {}