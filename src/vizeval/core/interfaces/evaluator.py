from abc import ABC, abstractmethod
from vizeval.core.entities import EvaluationResult, EvaluationRequest

class Evaluator(ABC):
    """Abstract base class for all evaluators."""

    name: str = "base"

    @abstractmethod
    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        raise NotImplementedError