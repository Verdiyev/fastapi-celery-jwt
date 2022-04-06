
import secrets
from urllib import response
import celery
from fastapi import  FastAPI, Depends, HTTPException, Request, status
from auth import authenticate
from database import *
from peewee import *
from schemas import User
from fastapi.responses import JSONResponse
from fastapi_jwt_auth.exceptions import AuthJWTException
from config import settings
from fastapi_jwt_auth import AuthJWT
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from celery.result import AsyncResult
from worker_task import get_ip_details, celery

import crud, models, schemas 

from fastapi.routing import APIRoute

import inspect, re
from fastapi.openapi.utils import get_openapi


db.connect()
db.create_tables([models.User, models.IpDetail])
db.close()


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"} 
 

@AuthJWT.load_config
def get_config():
    return settings


# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )



# provide a method to create access tokens. The create_access_token()
# function is used to actually generate the token to use authorization
# later in endpoint protected
@app.post('/api/v1/login')
def login(user: schemas.UserCreate, Authorize: AuthJWT = Depends(), ):
    
    if not authenticate(user.username, user.password):
        raise HTTPException(status_code=401,detail="Bad username or password")

    # subject identifier for who this token is for example id or username from database
    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)
    return {"access_token": access_token, "refresh_token": refresh_token}

# protect endpoint with function jwt_required(), which requires
# a valid access token in the request headers to access.
@app.get('/api/v1/user')
def user(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}

@app.on_event("startup")
def startup():
    if db.is_closed():
        db.connect()
    

@app.on_event("shutdown")
def shutdown():
    print("Closing...")
    if not db.is_closed():
        db.close()

@app.post('/api/v1/signup', response_model=schemas.User)
def create_user(user: schemas.UserCreate):
    db_user = crud.get_user_by_username(username= user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="username already registered")
    return crud.create_user(user=user)




@app.get('/api/v1/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    """
    The jwt_refresh_token_required() function insures a valid refresh
    token is present in the request before running any code below that function.
    we can use the get_jwt_subject() function to get the subject of the refresh
    token, and use the create_access_token() function again to make a new access token
    """
    Authorize.jwt_refresh_token_required()
    current_user = Authorize.get_jwt_subject()
    new_access_token = Authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}

@app.post("/api/v1/task")
async def create_task(ip: schemas.Ip):
    
    
    task = get_ip_details.delay(ip.address)

    result = task.get()
    ip_obj = models.IpDetail(
        ip=ip.address,
        details=result
    )
    ip_obj.save()
    
    return {"task_id": task.id}

@app.get("/api/v1/status/{id}")
async def check_task_status(id:str):
    result = AsyncResult(id, app=celery)
    return {"status": result.state}

#custom open api to include authorization header in swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title = "My Auth API",
        version = "1.0",
        description = "An API with an Authorize Button",
        routes = app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token"
        }
    }

    # Get all routes where jwt_optional() or jwt_required
    api_router = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_router:
        path = getattr(route, "path")
        endpoint = getattr(route,"endpoint")
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            # access_token
            if (
                re.search("jwt_required", inspect.getsource(endpoint)) or
                re.search("fresh_jwt_required", inspect.getsource(endpoint)) or
                re.search("jwt_optional", inspect.getsource(endpoint))
            ):
                openapi_schema["paths"][path][method]["security"] = [
                    {
                        "Bearer Auth": []
                    }
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
























