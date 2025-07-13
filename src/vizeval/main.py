from fastapi import FastAPI
from dotenv import load_dotenv
import threading

# Routes
from vizeval.app.api.routes.evaluation import router as evaluation_router
from vizeval.app.api.routes.user import router as user_router

# Services and dependencies
from vizeval.infrastructure.memory_repository import MemoryRepository
from vizeval.infrastructure.queue.memory_queue import MemoryQueue

# Load environment variables
load_dotenv()

# Initialize application
app = FastAPI(
    title="VizEval API",
    description="API for evaluating model outputs",
    version="0.1.0",
)

# Initialize dependencies
repository = MemoryRepository()
queue = MemoryQueue()

# Initialize services
from vizeval.app.services.service_provider import initialize_services, get_evaluation_service
initialize_services(repository, queue)

# Include routers
app.include_router(evaluation_router)
app.include_router(user_router)

# Start the evaluation worker in a separate thread
worker_thread = None


@app.get("/")
async def root():
    return {"message": "Welcome to VizEval API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


def start_worker_thread():
    evaluation_service = get_evaluation_service()
    evaluation_service.start_worker()


@app.on_event("startup")
async def startup_event():
    global worker_thread
    worker_thread = threading.Thread(target=start_worker_thread, daemon=True)
    worker_thread.start()
    print("Evaluation worker started in background thread")


@app.on_event("shutdown")
async def shutdown_event():
    evaluation_service = get_evaluation_service()
    evaluation_service.stop_worker()
    if worker_thread and worker_thread.is_alive():
        worker_thread.join(timeout=5.0)
    print("Evaluation worker stopped")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("vizeval.main:app", host="0.0.0.0", port=8000, reload=True)
