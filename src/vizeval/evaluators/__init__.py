from typing import Dict

from .dummy import DummyEvaluator
from .juridical import JuridicalEvaluator
from .base import BaseEvaluator

_evaluators: Dict[str, BaseEvaluator] = {
    DummyEvaluator.name: DummyEvaluator(),
    JuridicalEvaluator.name: JuridicalEvaluator(),
}


def get_evaluator(name: str) -> BaseEvaluator:
    """Retrieve evaluator instance by name, defaulting to dummy evaluator."""
    return _evaluators.get(name, _evaluators[DummyEvaluator.name])

print("AVAILABLE EVALUATORS:", _evaluators.keys())