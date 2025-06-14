from app.routes import auth  # <- make sure `tasks.py` exists and has a router
from app.web_app import view_tasks as tasks
from app.web_app import reset_pwd
from app.web_app import assign_tasks
from app.web_app import confirm_tasks
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
 

app = FastAPI()

app.include_router(auth.router)
app.include_router(tasks.router)  # <- this line is critical
app.include_router(reset_pwd.router)
app.include_router(assign_tasks.router)
app.include_router(confirm_tasks.router)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/login")
