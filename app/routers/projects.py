from fastapi import APIRouter
from app.lib.utils.customRoute import CustomRoute
from app.routers.projectRouters import (
    base,
    essential_contacts,
    iam,
    dataGroups,
)

router = APIRouter(prefix="/projects", route_class=CustomRoute)


router.include_router(base.subrouter, tags=["projets/base"])
router.include_router(
    essential_contacts.subrouter,
    prefix="/{project_id}/essential_contacts",
    tags=["projets/essentialContacts"],
)
router.include_router(
    iam.subrouter, prefix="/{project_id}/iam", tags=["projets/iam"]
)
router.include_router(
    dataGroups.subrouter,
    prefix="/{project_id}/datagroups",
    tags=["projets/datagroups"],
)
