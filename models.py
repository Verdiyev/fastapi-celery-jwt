from enum import Enum
from database import db
from peewee import Model, CharField
from typing import Optional
from pydantic import BaseModel


class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        db_table = 'users'

class Task(BaseModel):
    ip = CharField(null=False,  max_length=255)
    details = CharField(null=False,  max_length=255)

    class Meta:
        db_table = 'tasks'

