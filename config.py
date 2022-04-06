from pydantic import BaseModel

class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    db_user='root'
    db_name='whelp'
    db_host='localhost'
    db_pass='root'
    db_port = 3306
    IP_API_KEY= 'ca0d0d966ff24ebf73d3364b9bbcc600df9cd1a5abd77ce5f9949640'
    CELERY_BROKER_URL= 'amqp://guest:guest@127.0.0.1:5672//'
    CELERY_RESULT_BACKEND= 'db+mysql://root:root@localhost:3306/whelp'

settings = Settings()