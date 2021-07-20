from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from .db import database, metadata, engine
from .models import SelectedDateModel
from .schemas import CreateSchema
from .services import write_table

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.state.database = database
metadata.create_all(engine)


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()


@app.get('/')
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/add/')
async def add(request: Request):
    return templates.TemplateResponse("add.html", {"request": request})


@app.get('/api/date/')
async def get_date():
    date = await SelectedDateModel.objects.all()
    return {'date': date}


@app.post('/api/add/')
async def add_reception(data: CreateSchema):
    try:

        await SelectedDateModel.objects.create(datetime=data.datetime)
        if not write_table(data.fio, data.datetime):
            return {'success': False, 'detail': "Ошибка сервера"}

        return {'success': True}
    except Exception as e:
        return {'success': False, 'detail': "Это время уже забронировано"}
