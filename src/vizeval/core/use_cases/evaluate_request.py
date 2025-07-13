from vizeval.core.entities import EvaluationRequest, EvaluationResult, Evaluation
from vizeval.core.interfaces import VizevalRepository, Evaluator

class EvaluateRequest:
    def __init__(self, evaluator: Evaluator, repository: VizevalRepository):
        self.evaluator = evaluator
        self.repository = repository
    
    def execute_fast_eval(self, request: EvaluationRequest) -> EvaluationResult:
        evaluation_result = self.evaluator.fast_evaluate(request)
        return evaluation_result

    def execute_detailed_eval(self, request: EvaluationRequest) -> EvaluationResult:
        fast_evaluation_result = self.evaluator.fast_evaluate(request)
        detailed_evaluation_result = self.evaluator.detailed_evaluate(request)

        evaluation = self._build_evaluation(request, detailed_evaluation_result, fast_evaluation_result)
        self.repository.store_evaluation(evaluation)
        return detailed_evaluation_result

    def _build_evaluation(self, request: EvaluationRequest, 
                            detailed_eval_result: EvaluationResult,
                            fast_eval_result: EvaluationResult) -> Evaluation:
        return Evaluation(
            system_prompt=request.system_prompt,
            user_prompt=request.user_prompt,
            response=request.response,
            evaluator=request.evaluator,
            user_id=request.user_id,
            metadata=request.metadata,
            score=fast_eval_result.score,
            feedback=detailed_eval_result.feedback
        )