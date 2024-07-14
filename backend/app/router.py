from fastapi import APIRouter

from app.controllers import (
    auth_controller,
    config_operation_controller,
    file_operation_controller,
    graph_controller,
)

api_router = APIRouter()
api_router.include_router(auth_controller.router, tags=["auth"])
api_router.include_router(graph_controller.router, tags=["graph"])
api_router.include_router(file_operation_controller.router, tags=["operation/file"])
api_router.include_router(config_operation_controller.router, tags=["operation/config"])
