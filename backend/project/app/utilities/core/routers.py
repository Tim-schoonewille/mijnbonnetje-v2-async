import os

from fastapi import FastAPI

from app.config import ROUTERS_ROOT_PATH as ROOT_PATH
from app.config import ROUTERS_EXCLUDE_FOLDERS as EXCLUDE_FOLDERS
from app.config import ROUTERS_EXCLUDE_FILES as EXCLUDE_FILES


def init_routers_old(app: FastAPI):
    sub_folders = [
        folder
        for folder in os.listdir(ROOT_PATH)
        if os.path.isdir(os.path.join(ROOT_PATH, folder))
        and folder not in EXCLUDE_FOLDERS
    ]
    folders = ['.', *sub_folders]

    for folder in folders:
        if folder == '.':
            router_path = 'app.routers.'
        else:
            router_path = f'app.routers.{folder}.'

        router_files = [
            filename[:-3]
            for filename in os.listdir(ROOT_PATH + '/' + folder)
            if filename.endswith('.py') and filename not in EXCLUDE_FILES
        ]

        for router_name in router_files:
            router_module = __import__(router_path + router_name, fromlist=['router'])
            router = router_module.router
            app.include_router(router)


def init_routers(app: FastAPI, folder: str = ""):
    current_folder = os.path.join(ROOT_PATH, folder)
    sub_folders = [
        sub_folder
        for sub_folder in os.listdir(current_folder)
        if os.path.isdir(os.path.join(current_folder, sub_folder))
        and sub_folder not in EXCLUDE_FOLDERS
    ]

    router_path = "app.routers." + (folder + "." if folder else "")
    router_files = [
        filename[:-3]
        for filename in os.listdir(current_folder)
        if filename.endswith(".py") and filename not in EXCLUDE_FILES
    ]
    router_import_path = router_path.replace('/', '.')
    for router_name in router_files:
        router_module = __import__(router_import_path + router_name, fromlist=["router"])
        router = router_module.router
        app.include_router(router)

    for sub_folder in sub_folders:
        new_folder = os.path.join(folder, sub_folder) if folder else sub_folder
        init_routers(app, new_folder)
