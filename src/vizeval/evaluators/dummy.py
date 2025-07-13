import random
from typing import Dict, Any

from .base import BaseEvaluator

class DummyEvaluator(BaseEvaluator):
    name = "dummy"

    def evaluate(self, prompt: str, output: str, model_name: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        # Very naive evaluation: random score and generic feedback
        score = random.uniform(0, 1)
        feedback = "This is a dummy evaluation. Replace with domain-specific logic."
        return {
            "score": score,
            "feedback": feedback,
            "evaluator": self.name,
            "details": {}
        } 