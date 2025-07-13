from typing import Dict

from .dummy import DummyEvaluator
from .base import BaseEvaluator
from .medical_temp import MedicalEvaluator as MedicalEvaluatorTemp
# from .medical import MedicalEvaluator # Thats our real evaluator

_evaluators: Dict[str, BaseEvaluator] = {
    DummyEvaluator.name: DummyEvaluator(),
    MedicalEvaluatorTemp.name: MedicalEvaluatorTemp(),
}


def get_evaluator(name: str) -> BaseEvaluator:
    """Retrieve evaluator instance by name, defaulting to dummy evaluator."""
    return _evaluators.get(name, _evaluators[DummyEvaluator.name])
