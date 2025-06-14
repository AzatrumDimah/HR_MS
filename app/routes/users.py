from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.supabase_client import supabase
import bcrypt

default_password = "test123"
password_hash = bcrypt.hashpw(default_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})


@router.post("/add_user", response_class=HTMLResponse)
async def add_user(
    request: Request,
    name: str = Form(...),
    id_number: str = Form(...),
    group: str = Form(...),
    division: str = Form(...),
    section: str = Form(...),
    phone_number: str = Form(...),
    age: int = Form(...)
):  
    

    data = {
            "name": name,
            "id_number": id_number,
            "group_name": group,
            "division": division,
            "section": section,
            "phone_number": phone_number,
            "age": age,
            "password_hash":password_hash
        }

    print(data)
    
    try:
        # Check for duplicate ID or phone number
        id_check = supabase.table("users").select("id").eq("id_number", id_number).execute()
        phone_check = supabase.table("users").select("id").eq("phone_number", phone_number).execute()

        if id_check.data:
            return templates.TemplateResponse("create_user.html", {
                "request": request,
                "message": f"❌ ID number {id_number} already exists."
            })

        if phone_check.data:
            return templates.TemplateResponse("create_user.html", {
                "request": request,
                "message": f"❌ Phone number {phone_number} already exists."
            })
        # Insert new user
        supabase.table("users").insert([data]).execute()
        
        return templates.TemplateResponse("create_user.html", {
            "request": request,
            "message": "✅ User added successfully!"
        })

    except Exception as e:
        return templates.TemplateResponse("create_user.html", {
            "request": request,
            "message": f"⚠️ Error: {str(e)}"
        })
