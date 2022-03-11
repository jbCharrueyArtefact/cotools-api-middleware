from fastapi import FastAPI
from app.lib.utils.secret import get_sa_info, get_secrets
from app.routers import projects, basicat, folders, groups, roles


app = FastAPI()


app.include_router(projects.router)
app.include_router(basicat.router)
app.include_router(folders.router)
app.include_router(groups.router)
app.include_router(roles.router)
