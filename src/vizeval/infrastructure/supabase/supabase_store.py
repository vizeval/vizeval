from typing import List, Optional, Dict, Any
from uuid import uuid4

from supabase import create_client, Client

from vizeval.core.interfaces import VizevalRepository
from vizeval.core.entities import Evaluation, User
from vizeval.infrastructure.supabase.models.evaluation_model import EvaluationModel


class SupabaseStore(VizevalRepository):
    def __init__(self, supabase_url: str, supabase_key: str):
        self.client: Client = create_client(supabase_url, supabase_key)
    
    def store_evaluation(self, evaluation: Evaluation) -> str:
        evaluation_id = str(uuid4())
        
        evaluation_data = {
            "id": evaluation_id,
            "system_prompt": evaluation.system_prompt,
            "user_prompt": evaluation.user_prompt,
            "response": evaluation.response,
            "user_id": evaluation.user_id,
            "evaluator": evaluation.evaluator,
            "score": evaluation.score,
            "feedback": evaluation.feedback,
            "metadata": evaluation.metadata
        }
        
        self.client.table("evaluations").insert(evaluation_data).execute()
        
        return evaluation_id
    
    def get_evaluation(self, evaluation_id: str) -> Optional[Evaluation]:
        response = self.client.table("evaluations").select("*").eq("id", evaluation_id).execute()
        
        if not response.data:
            return None
        
        evaluation_data = response.data[0]
        evaluation_model = EvaluationModel(**evaluation_data)
        
        return Evaluation(
            system_prompt=evaluation_model.system_prompt,
            user_prompt=evaluation_model.user_prompt,
            response=evaluation_model.response,
            user_id=evaluation_model.user_id,
            evaluator=evaluation_model.evaluator,
            score=evaluation_model.score,
            feedback=evaluation_model.feedback,
            metadata=evaluation_model.metadata
        )
    
    def list_evaluations(self, user_id: str, limit: int = 100, offset: int = 0) -> List[Evaluation]:
        response = self.client.table("evaluations").select("*").eq("user_id", user_id).range(offset, offset + limit - 1).execute()
        
        if not response.data:
            return []
        
        evaluations = []
        for evaluation_data in response.data:
            evaluation_model = EvaluationModel(**evaluation_data)
            evaluation = Evaluation(
                system_prompt=evaluation_model.system_prompt,
                user_prompt=evaluation_model.user_prompt,
                response=evaluation_model.response,
                user_id=evaluation_model.user_id,
                evaluator=evaluation_model.evaluator,
                score=evaluation_model.score,
                feedback=evaluation_model.feedback,
                metadata=evaluation_model.metadata
            )
            evaluations.append(evaluation)
        
        return evaluations
    
    def get_user_from_api_key(self, api_key: str) -> Optional[str]:
        response = self.client.table("users").select("id").eq("api_key", api_key).execute()
        
        if not response.data:
            return None
        
        return response.data[0]["id"]
    
    def add_user(self, user: User) -> str:
        user_data = {
            "id": user.id,
            "name": user.name,
            "api_key": user.api_key
        }
        
        self.client.table("users").insert(user_data).execute()
        
        return user.api_key
