from app.routes import users, admin_rights
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

app = FastAPI()

# Mount static files (optional, e.g., CSS or JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(users.router)
app.include_router(admin_rights.router)



@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse("/create_user")  # or "/assign_admin"
