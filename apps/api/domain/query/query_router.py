from fastapi import APIRouter
from utils.supabase import supabase

router = APIRouter(
    prefix="/api/query",
)


@router.get("/list")
def query_list():
    queries = supabase.table("queries").select("*").execute()
    return queries


@router.post("/run")
def query_run():
    return {"data": "question_list"}
