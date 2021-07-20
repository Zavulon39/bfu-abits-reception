import datetime
from pydantic import BaseModel


class CreateSchema(BaseModel):
    fio: str
    datetime: datetime.datetime
