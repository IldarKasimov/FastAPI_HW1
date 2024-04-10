from fastapi import FastAPI, HTTPException, Request
from typing import Optional
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory='Seminars/5HW/templates')


class Users(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    password: str


user1 = Users(id=1, name='Ivan', email='ivan@mail.ru', password='1234qwer')
user2 = Users(id=2, name='Petr', email='petr@gmail.com', password='qwer')

users = [user1, user2]


@app.get('/users/')
async def get_user():
    return users


#  Задача 3


@app.post('/users/')
async def add_user(user: Users):
    users.append(user)
    return user


#  Задача 4


@app.put('/users/{name}/{password}')
async def update_user(name: str, password: str, user: Users):
    for i in range(len(users)):
        if users[i].name == name and users[i].password == password:
            users[i] = user
    return user


#  Задача 5


@app.delete('/users/{email}/{password}')
async def del_user(email: str, password: str):
    for i in range(len(users)):
        if users[i].email == email and users[i].password == password:
            return users.pop(i)
    return HTTPException(status_code=404, detail='Movie not found')


#  Задача 6

@app.get('/', response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse('temp_form.html', {'request': request, 'users': users})


@app.post('/add_user/')
async def add_user(request: Request):
    new_user = await request.form()
    if new_user.get('id') and new_user.get('name') and new_user.get('email') and new_user.get('password'):
        users.append(new_user)
        return f'Добавили пользователя: {new_user.get('name')}'  # нужно прейти на главную и обновить))
    return 'Заполните поля ввода'
