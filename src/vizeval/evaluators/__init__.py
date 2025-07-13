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


def register_evaluator(evaluator: BaseEvaluator):
    """Register a custom evaluator instance at runtime."""
    _evaluators[evaluator.name] = evaluator 