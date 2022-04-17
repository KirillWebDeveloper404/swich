from peewee import *
from .BaseModel import BaseModel


class ADS_db(BaseModel):

    name = TextField(null=False, column_name='name')
    phone = TextField(null=False, column_name='phone')
    addres = TextField(null=True, column_name='address')
    link = TextField(null=True, column_name='link')
    desc = TextField(null=True, column_name='desc')

    class Meta:

        table_name = 'ads'


try:
    ADS_db.create_table()
except:
    pass