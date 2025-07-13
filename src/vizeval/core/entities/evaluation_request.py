from typing import Optional, Dict
from dataclasses import dataclass

@dataclass
class EvaluationRequest:
    system_prompt: str
    user_prompt: str
    response: str
    metadata: Optional[Dict[str, str]] = None
    evaluator: str = "dummy"
    user_id: str = ""