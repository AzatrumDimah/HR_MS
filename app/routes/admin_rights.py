from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.supabase_client import supabase

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/admin_rights", response_class=HTMLResponse)
async def assign_admin_page(request: Request):
    return templates.TemplateResponse("assign_admin.html", {"request": request})

@router.post("/assign_admin_manual", response_class=HTMLResponse)
async def assign_admin_manual(
    request: Request,
    admin_id_number: str = Form(...),
    target_id_number: str = Form(...)
):
    try:
        # Fetch user and admin
        admin = supabase.table("users").select("id", "name").eq("id_number", admin_id_number).single().execute()
        target = supabase.table("users").select("id", "name").eq("id_number", target_id_number).single().execute()

        if not admin.data:
            return templates.TemplateResponse("assign_admin.html", {"request": request, "message": "❌ Admin ID not found."})
        if not target.data:
            return templates.TemplateResponse("assign_admin.html", {"request": request, "message": "❌ Target user ID not found."})

        if admin.data["id"] == target.data["id"]:
            return templates.TemplateResponse("assign_admin.html", {"request": request, "message": "❌ Cannot assign yourself as admin over yourself."})

        supabase.table("admin_rights").insert({
            "admin_id": admin.data["id"],
            "managed_user_id": target.data["id"]
        }).execute()

        return templates.TemplateResponse("assign_admin.html", {
            "request": request,
            "message": f"✅ {target.data['name']} ({target_id_number}) added under admin rights of  {admin.data['name']}."
        })

    except Exception as e:
        return templates.TemplateResponse("assign_admin.html", {"request": request, "message": f"⚠️ Error: {str(e)}"})


@router.post("/assign_admin_bulk", response_class=HTMLResponse)
async def assign_admin_bulk(
    request: Request,
    admin_id_number: str = Form(...),
    group: str = Form(...),
    division: str = Form(...),
    section: str = Form(...)
):
    try:
        admin = supabase.table("users").select("id", "name").eq("id_number", admin_id_number).single().execute()
        if not admin.data:
            return templates.TemplateResponse("assign_admin.html", {"request": request, "message": "❌ Admin ID not found."})

        users = supabase.table("users").select("id", "name", "id_number").eq("group_name", group).eq("division", division).eq("section", section).execute()

        assigned = []
        for user in users.data:
            if user["id"] != admin.data["id"]:  # Avoid self
                supabase.table("admin_rights").insert({
                    "admin_id": admin.data["id"],
                    "managed_user_id": user["id"]
                }).execute()
                assigned.append(f"{user['name']} ({user['id_number']})")

        if not assigned:
            return templates.TemplateResponse("assign_admin.html", {"request": request, "message": "ℹ️ No users were assigned (perhaps only you matched the filter)."})

        return templates.TemplateResponse("assign_admin.html", {
            "request": request,
            "message": f"✅ {admin.data['name']} has been assigned: {', '.join(assigned)}"
        })

    except Exception as e:
        return templates.TemplateResponse("assign_admin.html", {"request": request, "message": f"⚠️ Error: {str(e)}"})
