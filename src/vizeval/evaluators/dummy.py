import random
from typing import Dict, Any

from vizeval.evaluators.base import BaseEvaluator
from vizeval.core.entities import EvaluationRequest, EvaluationResult

class DummyEvaluator(BaseEvaluator):
    name = "dummy"

    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        # Very naive evaluation: random score and generic feedback
        score = random.uniform(0, 1)
        feedback = "This is a dummy evaluation. Replace with domain-specific logic."
        return EvaluationResult(
            score=score,
            feedback=feedback,
            evaluator=self.name,
        ) 