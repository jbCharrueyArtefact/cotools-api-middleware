from fastapi import FastAPI
from app.routers import projects, basicat, folders, groups, roles


app = FastAPI()

app.include_router(projects.router)
app.include_router(basicat.router)
app.include_router(folders.router)
app.include_router(groups.router)
app.include_router(roles.router)
