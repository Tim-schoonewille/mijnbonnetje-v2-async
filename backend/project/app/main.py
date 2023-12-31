import logging
import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.utilities.core.open_api import custom_generate_unique_id
from app.utilities.core.routers import init_routers


log = logging.getLogger("uvicorn")


def create_application(testing: bool = False) -> FastAPI:
    static_folder_path = "." + settings.STATIC_FOLDER
    if not os.path.exists(static_folder_path):
        os.makedirs(static_folder_path)

    origins = [
        "http://frontend.localhost:3000",
        "http://mijnbonnetje.lan:3000",
        "http://frontend.mijnbonnetje.lan:3000",
        "http://frontend.mijnbonnetje.nl:3000",
    ]
    application = FastAPI(
        title="mijnbonnetje.nl",
        generate_unique_id_function=custom_generate_unique_id)
    application.mount(
        settings.STATIC_FOLDER,
        StaticFiles(directory=f".{settings.STATIC_FOLDER}"),
        name="static",
    )
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
    # from app.utilities.core.redis import cache
    # cache().flushdb()


@app.on_event("shutdown")
async def shutdown_event():
    log.info("[+] Closing application...")
