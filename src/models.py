import datetime as dt
import ormar
from .db import metadata, database


class SelectedDateModel(ormar.Model):

    class Meta(ormar.ModelMeta):
        metadata = metadata
        database = database

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    datetime: dt.datetime = ormar.DateTime(unique=True)
