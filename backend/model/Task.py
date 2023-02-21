from typing import List
from pydantic import BaseModel
class Task(BaseModel):
    url: str
    keywords: List[str]
    status: str
    type: int
    # type 1 jd
    # type 2 news
    # type 3 weibo
