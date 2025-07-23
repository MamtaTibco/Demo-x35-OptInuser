"""FastAPI application factory and server configuration."""
from fastapi import FastAPI
import logging
from routes.api.v1.optin_user import router as optin_user_router
import logging
import uuid
from datetime import datetime
from typing import Optional, Dict, List

import httpx
import json
import pyodbc
from fastapi import FastAPI, HTTPException, Path, status
from pydantic import BaseModel, ValidationError
import logging
import uuid

import uvicorn
from fastapi import FastAPI
from x35_json_logging import initialize_logging, trace_id_var

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from x35_json_logging import initialize_logging, dynamic_context
from lookup.database import get_lookup_session, LookupDatabaseEngine
from settings import settings
from lookup.cache_service import run_select_and_cache
from src.exception import DBException


initialize_logging()

logger = logging.getLogger(f"x35.{__name__}")



@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with get_lookup_session() as session:
            cache_configurations = [
                ("select  A15_SITEID as  A15_SITEID, A15_SITE_GROUP as A15_SITE_GROUP from STERLING_A15_BRAND", "STERLING_A15_BRAND",),


                (
                    "select BRAND as BRAND, SOURCE as SOURCE, SITEID as SITEID ,SOURCE_EMS as SOURCE_EMS , DOUBLEOPTINFLAG as DOUBLEOPTINFLAG from OPTINTABLE_SOURCE",
                    "OPTINTABLE_SOURCE",
                ),

                ( "select BRAND_NAME as BRAND_NAME, STERLING_BRAND_CODE as STERLING_BRAND_CODE from BRAND_NAME_XREF",
                    "BRAND_NAME_XREF",
                ),

            ]
            for query, table_name in cache_configurations:
                run_select_and_cache(session, query, table_name)

            # DatabaseEngine.get_onsie_engine()
            LookupDatabaseEngine.get_lookup_engine()

    except DBException as e:
        logger.error(str(e), extra=e.extra, exc_info=True)
        raise e
    except Exception as e:
        logger.error(
            "Exception while loading the lookup data on server startup: %s",
            str(e),
            exc_info=True,
        )
        raise

    yield


class CustomHeaderMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add or propagate an X-Trace-ID header for request tracing.

    If the incoming request does not have an X-Trace-ID header, a new UUID is generated.
    The trace ID is attached to the response and used for logging context.
    """

    async def dispatch(self, request: Request, call_next):
        trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
        with dynamic_context(trace_id=trace_id):
            response = await call_next(request)
            response.headers["X-Trace-ID"] = trace_id
            return response


def create_app() -> FastAPI:
    """
    FastAPI application factory.

    Configures the FastAPI app, adds middleware, and includes all routers for health, metrics, version, and wholesale cost APIs.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI(
        docs_url="/docs" if settings.fastapi.enable_docs else None,
        redoc_url="/redoc" if settings.fastapi.enable_docs else None,
        lifespan=lifespan,
    )

    # Add middleware here
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(CustomHeaderMiddleware)





    app.include_router(optin_user_router)
    return app


if __name__ == "__main__":
    trace_id_var.set(str(uuid.uuid4()))
    logger.info("Starting FastAPI application")
    uvicorn.run(
        "app:create_app",
        factory=True,
        access_log=settings.uvicorn.access_log,
        backlog=settings.uvicorn.backlog,
        host="0.0.0.0",
        http=settings.uvicorn.http,
        limit_concurrency=settings.uvicorn.max_concurrency,
        log_level=settings.uvicorn.log_level,
        loop=settings.uvicorn.loop,
        port=settings.uvicorn.port,
        proxy_headers=settings.uvicorn.proxy_headers,
        reload=settings.uvicorn.reload,
        server_header=settings.uvicorn.server_header,
        timeout_keep_alive=settings.uvicorn.keep_alive,

    )
