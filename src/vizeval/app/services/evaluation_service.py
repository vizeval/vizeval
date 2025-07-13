import time
import signal

from vizeval.core.use_cases import EvaluateRequest
from vizeval.core.interfaces import VizevalRepository, Evaluator, EvaluationQueue
from vizeval.core.entities import EvaluationResult, EvaluationRequest


class EvaluationService:
    def __init__(self, evaluator: Evaluator, repository: VizevalRepository, queue: EvaluationQueue):
        self.evaluator = evaluator
        self.repository = repository
        self.queue = queue
        self._running = False
        
    def evaluate_sync(self, request: EvaluationRequest) -> EvaluationResult:
        evaluate_request = EvaluateRequest(self.evaluator, self.repository)
        return evaluate_request.execute(request)
        
    def evaluate_async(self, request: EvaluationRequest) -> None:
        """Add a request to the queue for asynchronous processing."""
        self.queue.enqueue(request)
    
    def start_worker(self, poll_interval: float = 5.0) -> None:
        """Start the worker to continuously process queued evaluation requests.
        
        Args:
            poll_interval: Time in seconds to wait between checking the queue when empty.
        """
        self._running = True
        print("Worker started. Press Ctrl+C to stop.")
        
        # Handle graceful shutdown on SIGINT (Ctrl+C)
        def signal_handler(signum, frame):
            print("\nShutting down worker...")
            self._running = False
        
        signal.signal(signal.SIGINT, signal_handler)
        
        while self._running:
            try:
                # Try to get a request from the queue
                if self.queue.is_empty():
                    time.sleep(poll_interval)
                    continue

                request = self.queue.dequeue()
                try:
                    # Process the request synchronously
                    result = self.evaluate_sync(request)
                    print(f"Processed evaluation request. Result score: {result.score}")
                except Exception as e:
                    print(f"Error processing evaluation request: {str(e)}")
            
            except KeyboardInterrupt:
                self._running = False
                print("\nWorker stopped by user.")

            except Exception as e:
                print(f"Unexpected error in worker: {str(e)}")
    
    def stop_worker(self) -> None:
        """Stop the worker on the next iteration."""
        self._running = False
