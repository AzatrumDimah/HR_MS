# supabase.py
from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv(".env")  # or "keys.env" if that's your file

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# print(supabase.table("users").select("*").limit(1).execute())

# result = supabase.table("users").insert({
#     "name": "Test User",
#     "id_number": "99999999",
#     "group_name": "Test Group",
#     "division": "Test Division",
#     "section": "Test Section",
#     "phone_number": "+910000000000",
#     "age": 30,
#     "password_hash": "dummyhash"
# }).execute()

# print(result)

# if SUPABASE_URL and SUPABASE_KEY and supabase:
#     print("✅ Supabase client initialized successfully.")
# else:
#     print("❌ Failed to initialize Supabase client.")