from fastapi import Response, status
from fastapi.routing import APIRouter

status_router = APIRouter(
    prefix="/status"
)

@status_router.get("")
def get_status(response: Response):
    response.status_code = status.HTTP_200_OK
    return response
