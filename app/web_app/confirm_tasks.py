from fastapi import APIRouter, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.supabase_client import supabase

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/confirm_tasks", response_class=HTMLResponse)
async def confirm_tasks_page(request: Request, user_id: str = Cookie(None)):
    if not user_id:
        return RedirectResponse("/login", status_code=303)

    try:
        rights_result = supabase.table("admin_rights") \
            .select("managed_user_id") \
            .eq("admin_id", user_id) \
            .execute()

        managed_user_ids = [entry["managed_user_id"] for entry in rights_result.data]

        users_tasks = []

        for uid in managed_user_ids:
            user_info = supabase.table("users").select("id, name").eq("id", uid).single().execute().data

            tasks_result = supabase.table("tasks") \
                .select("id, title, description, status") \
                .eq("assigned_to", uid) \
                .in_("status", ["in_progress", "completed"]) \
                .execute()

            users_tasks.append({
                "id": user_info["id"],
                "name": user_info["name"],
                "tasks": tasks_result.data
            })

        return templates.TemplateResponse("confirm_tasks.html", {
            "request": request,
            "users_tasks": users_tasks,
            "message": None
        })

    except Exception as e:
        return templates.TemplateResponse("confirm_tasks.html", {
            "request": request,
            "users_tasks": [],
            "message": f"⚠️ Error: {str(e)}"
        })


@router.post("/confirm_tasks/action", response_class=HTMLResponse)
async def handle_task_action(
    request: Request,
    task_id: str = Form(...),
    action: str = Form(...)
):
    try:
        if action == "confirm":
            supabase.table("tasks").update({"status": "confirmed"}).eq("id", task_id).execute()
        elif action == "reopen":
            supabase.table("tasks").update({"status": "in_progress"}).eq("id", task_id).execute()
        elif action == "complete":
            supabase.table("tasks").update({"status": "completed"}).eq("id", task_id).execute()

        return RedirectResponse("/confirm_tasks", status_code=303)

    except Exception as e:
        return templates.TemplateResponse("confirm_tasks.html", {
            "request": request,
            "users_tasks": [],
            "message": f"⚠️ Failed to update task: {str(e)}"
        })
