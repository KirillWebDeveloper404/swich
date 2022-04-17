from peewee import *
from .BaseModel import BaseModel


class User(BaseModel):
    tg_id = TextField(null=False, column_name='tg_id')
    photo = TextField(null=True, column_name='photo')
    name = TextField(null=True, column_name='name')
    phone = TextField(null=True, column_name='phone')
    tarif = TextField(null=True, column_name='tarif')
    dead_line = TextField(null=True, column_name='dead_line')

    length = TextField(null=True, column_name='lenght')
    weight = TextField(null=True, column_name='weight')
    age = TextField(null=True, column_name='age')
    field_activity = TextField(null=True, column_name='ocupation')
    profession = TextField(null=True, column_name='status')

    class Meta:
        table_name = 'users'


try:
    User.create_table()
except:
    pass