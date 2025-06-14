from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.supabase_client import supabase

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/my_tasks", response_class=HTMLResponse)
async def view_my_tasks(request: Request):
    current_user_id = request.cookies.get("user_id")
    current_user_name = request.cookies.get("user_name")
    print(current_user_id)

    if not current_user_id:
        return RedirectResponse(url="/login", status_code=302)

    response = supabase.table("tasks").select("*").eq("assigned_to", current_user_id).execute()
    tasks = response.data or []

    return templates.TemplateResponse("my_tasks.html", {
        "request": request,
        "tasks": tasks,
        "user_name": current_user_name,
        "message": None
    })


@router.post("/update_task_status", response_class=HTMLResponse)
async def update_task_status(request: Request, task_id: str = Form(...), new_status: str = Form(...)):
    current_user_id = request.cookies.get("user_id")

    if not current_user_id:
        return RedirectResponse(url="/login", status_code=302)

    supabase.table("tasks").update({"status": new_status}).eq("id", task_id).execute()
    return RedirectResponse(url="/my_tasks", status_code=303)
