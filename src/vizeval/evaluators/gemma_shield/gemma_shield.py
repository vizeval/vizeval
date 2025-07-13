from typing import Dict
import os

from transformers import AutoTokenizer
import torch

from vizeval.core.entities import EvaluationRequest


class GemmaShieldModel:
    name = "gemma_shield"
    
    def __init__(self, model_path: str):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = self._load_model(model_path)
        self.tokenizer = AutoTokenizer.from_pretrained("google/shieldgemma-2b")
        self.max_length = 1024
    
    def _load_model(self, model_path: str):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
            
        model = torch.jit.load(model_path, map_location=self.device)
        model.eval()
        return model
    
    def _prepare_input(self, request: EvaluationRequest) -> str:
        context = f"System: {request.system_prompt}\n\nUser: {request.user_prompt}\n\nResponse: {request.response}"
        return context
    
    def _tokenize(self, text: str) -> Dict[str, torch.Tensor]:
        encoded = self.tokenizer(text, 
                                 truncation=True, 
                                 padding="max_length", 
                                 max_length=self.max_length, 
                                 return_tensors="pt")
        return {
            "input_ids": encoded["input_ids"].to(self.device),
            "attention_mask": encoded["attention_mask"].to(self.device)
        }
    
    def evaluate(self, request: EvaluationRequest) -> str:
        """
        Evaluates a request and returns a string with an insight explanation for the response evaluated.
        
        Returns:
            A string containing an insight explanation for the response evaluated.
        """
        try:
            with torch.no_grad():
                input_text = self._prepare_input(request)
                tokens = self._tokenize(input_text)
                # TorchScript model expects positional arguments
                outputs = self.model(tokens["input_ids"], tokens["attention_mask"])
                
            return outputs[0].item()
            
        except Exception as e:
            return "Error at evaluate: " + str(e)