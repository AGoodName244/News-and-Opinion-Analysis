from fastapi import APIRouter
from app.controller import crawl_and_analyze

router = APIRouter()


router.post("/crawl_and_analyze")(crawl_and_analyze)
