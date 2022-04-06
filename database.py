import peewee
from config import settings
# class PeeweeConnectionState(peewee._ConnectionState):
#     def __init__(self, **kwargs):
#         super().__setattr__("_state", peewee.db_state)
#         super().__init__(**kwargs)

#     def __setattr__(self, name, value):
#         self._state.get()[name] = value

#     def __getattr__(self, name):
#         return self._state.get()[name]


db = peewee.MySQLDatabase(settings.db_name, user=settings.db_user, password=settings.db_pass,
                         host=settings.db_host, port=settings.db_port)
# db._state = PeeweeConnectionState()