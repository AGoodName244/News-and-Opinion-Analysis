from pydantic import BaseModel
from typing import Literal

class CrawlTask(BaseModel):
    task_id: str
    keyword: str
    source_url: str
    source_name: str
    depth: Literal["shallow", "medium", "deep"]