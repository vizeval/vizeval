from vizeval.evaluators.fastval import FastvalModel
from vizeval.evaluators.gemma_shield import GemmaShieldModel
from vizeval.evaluators.base import BaseEvaluator
from vizeval.core.entities import EvaluationRequest, EvaluationResult


class MedicalEvaluator(BaseEvaluator):
    """Evaluator especializado em conteúdo médico para detectar alucinações."""
    
    name = "medical"
    
    def __init__(self):
        self.fastval = FastvalModel(model_path="./models/fastval.pt")
        self.gemma_shield = GemmaShieldModel(model_path="./models/gemma_shield.pt")
            
    def fast_evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        """
        Use the custom Fastval model to evaluate the response and provide a risk level with low latency.
        """
        try:
            risk_score = self.fastval.evaluate(request)
            
            return EvaluationResult(
                score=risk_score,
                feedback=None,
                evaluator=self.name,
            )
            
        except Exception as e:
            return EvaluationResult(
                score=-1,
                feedback=f"Error at fast_evaluate: {str(e)}",
                evaluator=self.name,
            )

    def detailed_evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        try:
            feedback = self.fastval.evaluate(request)
            risk_score = self.gemma_shield.evaluate(request)
            
            return EvaluationResult(
                score=risk_score,
                feedback=feedback,
                evaluator=self.name,
            )
            
        except Exception as e:
            return EvaluationResult(
                score=-1,
                feedback=f"Error at detailed_evaluate: {str(e)}",
                evaluator=self.name,
            )