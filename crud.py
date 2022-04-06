import models, schemas
from auth import get_password_hash



def get_user(user_id: int):
    return models.User.get_by_id(1) 


def get_user_by_username(username: str):
    return models.User.filter(models.User.username == username).first()

def create_user(user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password) 
    db_user = models.User(username=user.username, password=hashed_password)
    db_user.save()
    return db_user