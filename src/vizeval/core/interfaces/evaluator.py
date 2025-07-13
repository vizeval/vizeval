from abc import ABC, abstractmethod
from vizeval.core.entities import EvaluationResult, EvaluationRequest

class Evaluator(ABC):
    """Abstract base class for all evaluators."""

    name: str = "base"

    @abstractmethod
    def fast_evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        raise NotImplementedError

    @abstractmethod
    def detailed_evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        raise NotImplementedError
    