from fastapi import APIRouter, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.supabase_client import supabase
import uuid

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/assign_tasks", response_class=HTMLResponse)
async def assign_tasks_page(request: Request, user_id: str = Cookie(None)):
    if not user_id:
        return RedirectResponse("/login", status_code=303)

    try:
        # Step 1: Get users managed by current user
        rights_result = supabase.table("admin_rights") \
            .select("managed_user_id") \
            .eq("admin_id", user_id) \
            .execute()
        managed_user_ids = [entry["managed_user_id"] for entry in rights_result.data]

        if not managed_user_ids:
            return templates.TemplateResponse("assign_tasks.html", {
                "request": request,
                "users_tasks": [],
                "admin_tasks": [],
                "message": "⚠️ You have no users under your management."
            })

        # Step 2: Get admin's own tasks to populate parent task dropdown
        admin_tasks_result = supabase.table("tasks") \
            .select("id, title") \
            .eq("assigned_to", user_id) \
            .eq("status", "in_progress") \
            .execute()
        admin_tasks = admin_tasks_result.data

        users_tasks = []

        for uid in managed_user_ids:
            user_info = supabase.table("users").select("id, name").eq("id", uid).single().execute().data

            tasks_result = supabase.table("tasks") \
                .select("id, title, description") \
                .eq("assigned_to", uid) \
                .eq("status", "in_progress") \
                .execute()

            users_tasks.append({
                "id": user_info["id"],
                "name": user_info["name"],
                "tasks": tasks_result.data
            })

        return templates.TemplateResponse("assign_tasks.html", {
            "request": request,
            "users_tasks": users_tasks,
            "admin_tasks": admin_tasks,
            "message": None
        })

    except Exception as e:
        return templates.TemplateResponse("assign_tasks.html", {
            "request": request,
            "users_tasks": [],
            "admin_tasks": [],
            "message": f"⚠️ Error: {str(e)}"
        })

@router.post("/assign_tasks/add", response_class=HTMLResponse)
async def add_task(
    request: Request,
    user_id: str = Cookie(None),
    target_user_id: str = Form(...),
    title: str = Form(...),
    description: str = Form(""),
    parent_task_id: str = Form(None)
):
    if not user_id:
        return RedirectResponse("/login", status_code=303)

    try:
        task_description = description if description.strip() != "" else title

        new_task = {
            "id": str(uuid.uuid4()),
            "title": title,
            "description": task_description,
            "assigned_to": target_user_id,
            "status": "in_progress",
            "parent_task_id": parent_task_id if parent_task_id != "None" else None
        }

        supabase.table("tasks").insert(new_task).execute()
        return RedirectResponse("/assign_tasks", status_code=303)

    except Exception as e:
        return templates.TemplateResponse("assign_tasks.html", {
            "request": request,
            "users_tasks": [],
            "admin_tasks": [],
            "message": f"⚠️ Failed to add task: {str(e)}"
        })
