import datetime
from pydantic import BaseModel


class CreateSchema(BaseModel):
    fio: str
    date: datetime.date
    time: datetime.time
