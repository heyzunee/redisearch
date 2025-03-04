from typing import List, Optional

from pydantic import BaseModel


class Movie(BaseModel):
    id: str
    title: str
    director: str
    genres: List[str]
    overview: Optional[str] = ""
    vote_average: float
    vote_count: Optional[int] = -1
