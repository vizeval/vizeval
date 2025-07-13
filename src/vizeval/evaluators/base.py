from abc import ABC, abstractmethod
from typing import Dict, Any

from vizeval.core.entities import EvaluationRequest, EvaluationResult

class BaseEvaluator(ABC):
    """Abstract base class for all evaluators."""

    name: str = "base"

    @abstractmethod
    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        """Return evaluation result as a dictionary."""
        raise NotImplementedError 