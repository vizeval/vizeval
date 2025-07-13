import time

from vizeval.core.use_cases import EvaluateRequest
from vizeval.core.interfaces import VizevalRepository, Evaluator, EvaluationQueue
from vizeval.core.entities import EvaluationResult, EvaluationRequest
from vizeval.evaluators import get_evaluator


class EvaluationService:
    def __init__(self, repository: VizevalRepository, queue: EvaluationQueue):
        self.repository = repository
        self.queue = queue
        self._running = False
        
    def evaluate(self, request: EvaluationRequest) -> EvaluationResult:
        evaluator = get_evaluator(request.evaluator)
        evaluate_request = EvaluateRequest(evaluator, self.repository)
        self.queue.enqueue(request)

        return evaluate_request.execute_fast_eval(request)
    
    def start_worker(self, poll_interval: float = 5.0) -> None:
        """Start the worker to continuously process queued evaluation requests.
        
        Args:
            poll_interval: Time in seconds to wait between checking the queue when empty.
        """
        self._running = True
        print("Evaluation worker started.")
        
        # We don't use signal handlers in threads as they only work in the main thread
        
        while self._running:
            try:
                # Try to get a request from the queue
                if self.queue.is_empty():
                    time.sleep(poll_interval)
                    continue

                request = self.queue.dequeue()
                try:
                    # Process the request synchronously
                    evaluator = get_evaluator(request.evaluator)
                    evaluate_request = EvaluateRequest(evaluator, self.repository)
                    result = evaluate_request.execute_detailed_eval(request)
                    print(f"Processed evaluation request in background thread. Result Feedback: {result.feedback}")

                except Exception as e:
                    print(f"Error processing evaluation request: {str(e)}")
            
            except Exception as e:
                print(f"Unexpected error in worker: {str(e)}")
                
        print("Evaluation worker stopped.")
    
    def stop_worker(self) -> None:
        """Stop the worker on the next iteration."""
        self._running = False
