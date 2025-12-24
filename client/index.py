from supabase import create_client
import os
from dotenv import load_dotenv


load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_ANON_KEY")

if not url or not key:
    print("[Exit] SUPABASE_URL or SUPABASE_ANON_KEY doesn't exist")
    exit(0)

supabase = create_client(url, key)
