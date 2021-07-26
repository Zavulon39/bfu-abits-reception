import datetime as dt
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
    data = await SelectedDateModel.objects.all()
    arr = []

    for i, d in enumerate(range(9, 32)):
        time = []
        date = dt.date(2021, 8, d)

        for t in range(9, 17):
            start_time = dt.time(t, 0, 0)
            end_time = dt.time(t + 1, 0, 0)

            matches_num = len(list(filter(lambda el: el.time == start_time and el.date == date, data)))

            time.append({
                'start_time': start_time,
                'end_time': end_time,
                'quantity': 10 - matches_num
            })

        arr.append({
            'date': date,
            'time': time
        })

    return templates.TemplateResponse("index.html", {"request": request, "arr": arr})


@app.post('/api/add/')
async def add_reception(data: CreateSchema):
    global idx
    try:
        await SelectedDateModel.objects.create(
            date=data.date,
            time=data.time
        )

        if write_table(data.fio, data.date, data.time):
            return {'success': True}

        return {'success': False, 'detail': 'Ошибка сервера'}
    except:
        return {'success': False, 'detail': 'Ошибка сервера'}
