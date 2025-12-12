from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes_health import router as health_router
from app.api.routes_projects import router as projects_router
from app.api.routes_generation import router as generation_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="TestOps Copilot Backend",
        version="0.1.0",
        description="Backend API for TestOps Copilot",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # для хакатона ставим широко
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(projects_router, prefix="/projects", tags=["projects"])
    app.include_router(generation_router, prefix="/generation", tags=["generation"])

    @app.get("/", tags=["root"])
    async def root():
        return {
            "message": "TestOps Copilot backend is running",
            "env": settings.app_env,
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.backend_host,
        port=settings.backend_port,
        reload=True,
    )
