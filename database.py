import peewee
from config import settings


db = peewee.MySQLDatabase(settings.db_name, user=settings.db_user, password=settings.db_pass,
                         host=settings.db_host, port=settings.db_port)
