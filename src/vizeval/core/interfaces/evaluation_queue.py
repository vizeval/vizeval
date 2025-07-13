from collections import deque
from typing import Deque

from vizeval.core.entities import EvaluationRequest


class EvaluationQueue:
    def __init__(self):
        self._queue: Deque[EvaluationRequest] = deque()
    
    def enqueue(self, evaluation_request: EvaluationRequest) -> None:
        self._queue.append(evaluation_request)
    
    def dequeue(self) -> EvaluationRequest:
        return self._queue.popleft()
    
    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def size(self) -> int:
        return len(self._queue)