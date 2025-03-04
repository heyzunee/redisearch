from typing import List

from pydantic import BaseModel
from src.schemas.schema import Movie


class BaseResponse(BaseModel):
    success: bool


class MovieResponse(BaseResponse):
    data: Movie


class MovieListResponse(BaseResponse):
    data: List[Movie]
