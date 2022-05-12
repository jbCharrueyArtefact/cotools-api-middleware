from fastapi import APIRouter, Depends
from app.dependencies import get_entities_client

from app.lib.utils.customRoute import CustomRoute


router = APIRouter(
    prefix="/entities", tags=["folders"], route_class=CustomRoute
)


@router.get("/")
def get_entities(entities_client=Depends(get_entities_client)):
    return entities_client.fetch_entities()
