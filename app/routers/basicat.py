from fastapi import APIRouter
from app.lib.utils.customRoute import CustomRoute
from app.lib.utils.secret import get_secrets
from app.clients import basicatClient

router = APIRouter(
    prefix="/basicat", tags=["basicat"], route_class=CustomRoute
)


@router.get("/{basicat}/")
def get_basicat_info(basicat: str):
    secret = get_secrets(secret="iosw")
    return basicatClient.get_basicat_info(
        secret["username"], secret["password"], basicat
    ).json()
