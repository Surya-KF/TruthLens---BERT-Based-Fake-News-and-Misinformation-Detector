from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.api import routes, auth_routes
from app.database import connect_to_mongodb, close_mongodb_connection


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle - connect/disconnect from MongoDB"""
    await connect_to_mongodb()
    yield
    await close_mongodb_connection()


app = FastAPI(
    title="Fake News Detection API",
    description="API for detecting fake news using fine-tuned BERT model with user authentication",
    version="2.0.0",
    lifespan=lifespan
)

# Configure CORS - update origins for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React dev server
        "http://localhost:5173",      # Vite dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "*"                           # Remove in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth_routes.router, prefix="/api", tags=["authentication"])
app.include_router(routes.router, prefix="/api", tags=["predictions"])

@app.get("/")
async def root():
    return {
        "message": "Fake News Detection API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
