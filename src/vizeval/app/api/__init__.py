from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from vizeval.api.routes import user, evaluation

app = FastAPI(
    title="VizEval API",
    description="API for evaluating model responses",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)
app.include_router(evaluation.router)


@app.get("/")
async def root():
    return {"message": "Welcome to VizEval API"}
