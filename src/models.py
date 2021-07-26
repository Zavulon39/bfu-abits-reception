import datetime as dt
import ormar
from .db import metadata, database


class SelectedDateModel(ormar.Model):

    class Meta(ormar.ModelMeta):
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    date: dt.date = ormar.Date(nullable=False)
    time: dt.time = ormar.Time(nullable=False)
