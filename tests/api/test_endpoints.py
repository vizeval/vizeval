import pytest
import requests
import subprocess
import time
import signal
import os
from urllib.parse import urljoin


class TestApiEndpoints:
    BASE_URL = "http://localhost:8000"
    server_process = None
    api_key = None
    
    # @classmethod
    # def setup_class(cls):
    #     # Start the FastAPI server
    #     cls.server_process = subprocess.Popen(
    #         ["uvicorn", "vizeval.main:app", "--host", "0.0.0.0", "--port", "8000"],
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE,
    #         preexec_fn=os.setsid
    #     )
    #     # Wait for server to start
    #     time.sleep(2)
    
    # @classmethod
    # def teardown_class(cls):
    #     # Terminate the server process
    #     if cls.server_process:
    #         os.killpg(os.getpgid(cls.server_process.pid), signal.SIGTERM)
    #         cls.server_process.wait()
    
    def test_create_user(self):
        """Test creating a user and getting an API key."""
        url = urljoin(self.BASE_URL, "/user/")
        payload = {"name": "Test User"}
        
        response = requests.post(url, json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert "name" in data
        assert "api_key" in data
        assert data["name"] == "Test User"
        
        # Save API key for other tests
        TestApiEndpoints.api_key = data["api_key"]
    
    def test_create_evaluation(self):
        """Test creating an evaluation synchronously."""
        url = urljoin(self.BASE_URL, "/evaluation/")
        payload = {
            "system_prompt": "You are a helpful assistant.",
            "user_prompt": "Tell me about Python.",
            "response": "Python is a programming language.",
            "evaluator": "dummy",
            "api_key": "mock-api-key",
            "async_mode": False
        }
        
        response = requests.post(url, json=payload)
        
        assert response.status_code == 201
        data = response.json()
        assert "evaluator" in data
        assert "score" in data
        assert "feedback" in data
    
    def test_get_user_evaluations(self):
        """Test retrieving evaluations for a user."""
        url = urljoin(self.BASE_URL, f"/user/evaluations?api_key={TestApiEndpoints.api_key}")
        
        response = requests.get(url)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "evaluator" in data[0]
            assert "score" in data[0]
            assert "feedback" in data[0]


if __name__ == "__main__":
    # This allows running the tests directly with python
    pytest.main(["-xvs", __file__])
