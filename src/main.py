# Established: 12/2/2020
from fastapi import FastAPI

from data import mongo_data
from models.settings import get_settings
from routers.channel_router import channel_router
from services.logging import get_logger


def setup_routing(api: FastAPI):
    api.include_router(channel_router)


def setup_events(api: FastAPI):
    api.add_event_handler("startup", mongo_data.connect)
    api.add_event_handler("shutdown",  mongo_data.close)


def get_application() -> FastAPI:    

    logger = get_logger()
    logger.debug('Setting up application ...')

    settings = get_settings()
    api = FastAPI(
        title=settings.project_name
    )

    setup_routing(api)
    setup_events(api)
    logger.info('Application setup complete ...')
    return api


if __name__ == "__main__":
    import uvicorn
    app = get_application()
    uvicorn.run(app)
