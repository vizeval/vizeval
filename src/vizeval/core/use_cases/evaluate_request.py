from vizeval.core.entities import EvaluationRequest, EvaluationResult, Evaluation
from vizeval.core.interfaces import VizevalRepository, Evaluator

class EvaluateRequest:
    def __init__(self, evaluator: Evaluator, repository: VizevalRepository):
        self.evaluator = evaluator
        self.repository = repository
    
    def execute(self, request: EvaluationRequest) -> EvaluationResult:
        evaluation_result = self.evaluator.evaluate(request)
        evaluation = self._build_evaluation(request, evaluation_result)
        self.repository.store_evaluation(evaluation)
        return evaluation_result

    def _build_evaluation(self, request: EvaluationRequest, result: EvaluationResult) -> Evaluation:
        return Evaluation(
            system_prompt=request.system_prompt,
            user_prompt=request.user_prompt,
            response=request.response,
            evaluator=request.evaluator,
            user_id=request.user_id,
            metadata=request.metadata,
            score=result.score,
            feedback=result.feedback
        )