from fastapi import Depends, FastAPI
from app.lib.utils.controls import is_allowed
from app.routers import projects, basicat, folders, groups, roles


app = FastAPI(dependencies=[Depends(is_allowed)])

app.include_router(projects.router)
app.include_router(basicat.router)
app.include_router(folders.router)
app.include_router(groups.router)
app.include_router(roles.router)
