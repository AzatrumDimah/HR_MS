# app/routers/password.py
from fastapi import APIRouter, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.supabase_client import supabase
import bcrypt

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/reset_password", response_class=HTMLResponse)
async def reset_password_form(request: Request):
    return templates.TemplateResponse("reset_password.html", {"request": request, "message": None})

@router.post("/reset_password", response_class=HTMLResponse)
async def reset_password(
    request: Request,
    old_password: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...),
    user_id: str = Cookie(None)
):
    if not user_id:
        return RedirectResponse("/login", status_code=303)

    if new_password != confirm_password:
        return templates.TemplateResponse("reset_password.html", {
            "request": request,
            "message": "❌ New password and confirmation do not match."
        })

    try:
        user = supabase.table("users").select("*").eq("id", user_id).single().execute().data

        if not bcrypt.checkpw(old_password.encode(), user["password_hash"].encode()):
            return templates.TemplateResponse("reset_password.html", {
                "request": request,
                "message": "❌ Old password is incorrect."
            })

        new_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
        supabase.table("users").update({"password_hash": new_hash}).eq("id", user_id).execute()

        return templates.TemplateResponse("reset_password.html", {
            "request": request,
            "message": "✅ Password updated successfully."
        })

    except Exception as e:
        return templates.TemplateResponse("reset_password.html", {
            "request": request,
            "message": f"⚠️ Error: {str(e)}"
        })
