from enum import Enum
from pydoc import describe
from pydantic import BaseModel
from pydantic.utils import GetterDict
import peewee as pw
from typing import Any, List, Optional

from fastapi_jwt_auth import AuthJWT

class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        if isinstance(res, pw.ModelSelect):
            return list(res)
        return res


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict

class Task(BaseModel):
    address: str



