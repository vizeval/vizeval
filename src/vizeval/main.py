from fastapi import FastAPI
from dotenv import load_dotenv

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
from vizeval.app.services.service_provider import initialize_services
initialize_services(repository, queue)

# Include routers
app.include_router(evaluation_router)
app.include_router(user_router)


@app.get("/")
async def root():
    return {"message": "Welcome to VizEval API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("vizeval.main:app", host="0.0.0.0", port=8000, reload=True)
