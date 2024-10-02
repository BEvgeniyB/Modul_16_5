
from fastapi import FastAPI, Path,HTTPException,Request
from fastapi.responses import HTMLResponse
from typing import Annotated
from fastapi.templating import Jinja2Templates

from pydantic import BaseModel, field_validator

app = FastAPI()
templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int = None

    @field_validator("username")
    def check_username(cls,value):
        if 5 <= len(value) <= 20:
            return value
        else:
            raise ValueError("Длина имени от 5 до 20 знаков")

    @field_validator("age")
    def check_age(cls, value):

        if 18 <= value <= 120:
            return value
        else:
            raise ValueError("Возраст от 18 до 120 лет")

@app.get("/")
async def all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html",{"request": request,"users": users})

@app.get("/user/{user_id}")
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse("users.html",{"request": request,"user": users[user_id-1]})


@app.delete('/user/{user_id}')
async def delete_user(user_id: int = Path(ge=1, le=100, description="Enter User ID", example="10")) -> str:
    try:
        user = [i for i in users if i.id == user_id][0]
        users.remove(user)
        return f"User {user} has been deleted"
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.post("/user/{username}/{age}")
async def add_user(user: User) ->str:
    if len(users) == 0:
        user.id = 1
    else:
        user.id = users[-1].id+1
    users.append(user)
    return f"User {user} is registered"



@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[ int,Path(ge=1, le=100, description="Enter User ID", example="10")],
                      username: Annotated[ str,Path(min_length=5, max_length=20, description="Enter username", example="UrbanUser")],
                      age: int = Path(ge=18, le=120, description="Enter age", example="24")) -> str:
    try:
        user = [i for i in users if i.id == user_id][0]
        user.username = username
        user.age = age
        return f"User {user} has been updated"
    except IndexError:
        raise HTTPException(status_code=404,detail="User was not found")


