from peewee import *
from .BaseModel import BaseModel


class Admin(BaseModel):
    tg_id = TextField(null=False, column_name='tg_id')

    class Meta:
        table_name = 'admins'


try:
    Admin.create_table()
except:
    pass