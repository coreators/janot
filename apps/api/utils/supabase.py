from supabase import create_client, Client
import os

url = os.environ["SUPABASE_BASE_URL"]
key = os.environ["SUPABASE_ANON_KEY"]

supabase: Client = create_client(url, key)
