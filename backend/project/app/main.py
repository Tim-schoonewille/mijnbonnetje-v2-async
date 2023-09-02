import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utilities.core.routers import init_routers


log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    origins = ['http://frontend.localhost:3000', 'http://dev.localhost:3000']
    application = FastAPI(title="mijnbonnetje.nl")
    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    init_routers(application)
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("[+] Starting application...")
    # from app.db import sync_create_tables
    # sync_create_tables(drop=True)
    # from app.db import create_tables
    # await create_tables(drop=True)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("[+] Closing application...")
