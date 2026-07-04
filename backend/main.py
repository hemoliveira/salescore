import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.database import DatabaseManager
from core.logger import Logger

from routes.customers import router as customers_router
from routes.health import router as health_router
from routes.orders import router as orders_router
from routes.products import router as products_router
from routes.dashboard import router as dashboard_router


logger = Logger.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown.
    """
    logger.info("Starting application...")

    try:
        logger.info("Initializing application infrastructure...")
        DatabaseManager.init_pool(pool_size=10)
        logger.info("Database pool initialized successfully.")
    except Exception as e:
        logger.exception("Bootstrap failed")
        raise RuntimeError("Application startup failed") from e

    try:
        yield
    finally:
        logger.info("Shutting down application...")
        DatabaseManager.close_pool()
        logger.info("Cleanup completed.")


app = FastAPI(
    title="Customer, Product & Order Management API",
    description="A professional CRUD system built with FastAPI and MySQL",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def _debug_exception_handler(request: Request, exc: Exception):
    # TEMPORARY: surfaces the real traceback in the response for prod debugging.
    return JSONResponse(
        status_code=500,
        content={
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback": traceback.format_exc(),
        },
    )


app.include_router(health_router, prefix="/api")
app.include_router(customers_router, prefix="/api")
app.include_router(products_router, prefix="/api")
app.include_router(orders_router, prefix="/api")
app.include_router(dashboard_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
