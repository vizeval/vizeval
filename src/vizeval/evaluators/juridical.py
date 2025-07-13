from typing import Dict, Any

from .base import BaseEvaluator

class JuridicalEvaluator(BaseEvaluator):
    """Evaluator specialized in juridical content analysis."""
    
    name = "juridical"
    
    def evaluate(self, prompt: str, output: str, model_name: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate LLM output from a juridical perspective.
        
        This is a simplified example. In a real implementation, this would use
        specialized juridical knowledge and potentially call external APIs or models
        trained specifically for legal content evaluation.
        """
        # Example evaluation logic for juridical content
        score = self._calculate_score(prompt, output)
        feedback = self._generate_feedback(score, output)
        details = self._analyze_details(prompt, output)
        
        return {
            "score": score,
            "feedback": feedback,
            "evaluator": self.name,
            "details": details
        }
    
    def _calculate_score(self, prompt: str, output: str) -> float:
        """
        Calculate a score based on juridical criteria.
        
        This is a simplified implementation. A real implementation would analyze:
        - Legal accuracy
        - Citation of relevant laws/precedents
        - Logical reasoning
        - Consideration of legal context
        - Etc.
        """
        # Simple scoring based on length and keyword presence
        # In a real implementation, this would use more sophisticated analysis
        
        # Check for common legal terms
        legal_terms = [
            "law", "legal", "court", "judge", "ruling", "statute", "regulation",
            "precedent", "jurisdiction", "plaintiff", "defendant", "contract",
            "liability", "rights", "obligation"
        ]
        
        term_count = sum(1 for term in legal_terms if term.lower() in output.lower())
        term_score = min(term_count / 5, 1.0)  # Cap at 1.0
        
        # Check for response length adequacy
        length_score = min(len(output) / 500, 1.0)  # Cap at 1.0
        
        # Combined score with weights
        return 0.6 * term_score + 0.4 * length_score
    
    def _generate_feedback(self, score: float, output: str) -> str:
        """Generate feedback based on the evaluation score."""
        if score > 0.8:
            return "Excellent legal analysis with proper terminology and adequate depth."
        elif score > 0.6:
            return "Good legal response but could benefit from more specific legal references or precedents."
        elif score > 0.4:
            return "Acceptable response but lacks sufficient legal depth and precision."
        else:
            return "Inadequate legal analysis. The response needs significant improvement in legal reasoning and terminology."
    
    def _analyze_details(self, prompt: str, output: str) -> Dict[str, str]:
        """Provide detailed analysis of different aspects of the legal response."""
        # In a real implementation, this would provide detailed analysis of:
        # - Legal accuracy
        # - Citation quality
        # - Reasoning structure
        # - Etc.
        
        return {
            "legal_terminology": self._evaluate_legal_terminology(output),
            "reasoning_structure": self._evaluate_reasoning(output),
            "prompt_relevance": self._evaluate_relevance(prompt, output)
        }
    
    def _evaluate_legal_terminology(self, output: str) -> str:
        """Evaluate the use of legal terminology."""
        legal_terms = [
            "law", "legal", "court", "judge", "ruling", "statute", "regulation",
            "precedent", "jurisdiction", "plaintiff", "defendant", "contract",
            "liability", "rights", "obligation"
        ]
        
        term_count = sum(1 for term in legal_terms if term.lower() in output.lower())
        
        if term_count > 10:
            return "Excellent use of legal terminology"
        elif term_count > 5:
            return "Good use of legal terminology"
        elif term_count > 2:
            return "Limited use of legal terminology"
        else:
            return "Insufficient legal terminology"
    
    def _evaluate_reasoning(self, output: str) -> str:
        """Evaluate the legal reasoning structure."""
        # Simple heuristic based on paragraph count
        paragraphs = [p for p in output.split("\n\n") if p.strip()]
        
        if len(paragraphs) > 3:
            return "Well-structured legal reasoning with multiple supporting points"
        elif len(paragraphs) > 1:
            return "Basic legal reasoning structure present"
        else:
            return "Insufficient reasoning structure"
    
    def _evaluate_relevance(self, prompt: str, output: str) -> str:
        """Evaluate how well the response addresses the legal question in the prompt."""
        # Simple check for prompt keywords in output
        prompt_words = set(prompt.lower().split())
        output_words = set(output.lower().split())
        
        common_words = prompt_words.intersection(output_words)
        relevance_ratio = len(common_words) / len(prompt_words) if prompt_words else 0
        
        if relevance_ratio > 0.7:
            return "Excellent relevance to the legal question"
        elif relevance_ratio > 0.5:
            return "Good relevance to the legal question"
        elif relevance_ratio > 0.3:
            return "Moderate relevance to the legal question"
        else:
            return "Poor relevance to the legal question"
