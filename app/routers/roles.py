from fastapi import APIRouter
import json

from app.lib.utils.customRoute import CustomRoute

router = APIRouter(prefix="/roles", tags=["roles"], route_class=CustomRoute)


@router.get("/")
def get_roles():
    with open("app/config/allRoles.json") as roles:
        return json.load(roles)


@router.get("/recommandation/")
def get_recommandation():
    with open("app/config/recoRoles.json") as roles:
        return json.load(roles)
