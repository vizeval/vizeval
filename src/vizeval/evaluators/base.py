from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseEvaluator(ABC):
    """Abstract base class for all evaluators."""

    name: str = "base"

    @abstractmethod
    def evaluate(self, prompt: str, output: str, model_name: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Return evaluation result as a dictionary."""
        raise NotImplementedError 