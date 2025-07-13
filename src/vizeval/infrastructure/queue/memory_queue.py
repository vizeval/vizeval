from collections import deque
from typing import Optional

from vizeval.core.interfaces.evaluation_queue import EvaluationQueue
from vizeval.core.entities.evaluation_request import EvaluationRequest


class MemoryQueue(EvaluationQueue):
    def __init__(self):
        self.queue = deque()
        
    def enqueue(self, evaluation_request: EvaluationRequest) -> None:
        self.queue.append(evaluation_request)
        
    def dequeue(self) -> Optional[EvaluationRequest]:
        if self.is_empty():
            return None
        return self.queue.popleft()
        
    def is_empty(self) -> bool:
        return len(self.queue) == 0
