# app/routers/auth.py

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.supabase_client import supabase
import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login_user(
    request: Request,
    id_number: str = Form(...),
    password: str = Form(...)
):
    try:
        result = supabase.table("users").select("*").eq("id_number", id_number).single().execute()
        user = result.data

        if not user:
            return templates.TemplateResponse("login.html", {
                "request": request,
                "message": "❌ ID not found."
            })

        if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
            return templates.TemplateResponse("login.html", {
                "request": request,
                "message": "❌ Incorrect password."
            })

        # ✅ Set cookies and redirect to tasks page
        response = RedirectResponse(url="/my_tasks", status_code=302)
        response.set_cookie(key="user_id", value=str(user["id"]))
        response.set_cookie(key="user_name", value=user["name"])
        return response

    except Exception as e:
        return templates.TemplateResponse("login.html", {
            "request": request,
            "message": f"⚠️ Error: {str(e)}"
        })
