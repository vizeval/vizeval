from dataclasses import dataclass
from typing import Optional

@dataclass
class EvaluationResult:
    evaluator: str
    score: Optional[float] = None
    feedback: Optional[str] = None
