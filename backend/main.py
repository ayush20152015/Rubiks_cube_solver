from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routes import cube
import os

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="Rubik's Cube Solver using CNN + IDA* Algorithm"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(cube.router, prefix=settings.API_PREFIX)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        'name': settings.API_TITLE,
        'version': settings.API_VERSION,
        'docs': '/docs'
    }


@app.get("/health")
async def health():
    """Health check"""
    return {'status': 'ok'}


if __name__ == "__main__":
    import uvicorn
    
    # Create models directory if it doesn't exist
    os.makedirs(settings.MODEL_DIR, exist_ok=True)
    
    # Run server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
