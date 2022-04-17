from peewee import *
from .BaseModel import BaseModel


class IventStatistic(BaseModel):
    place_id = TextField(null=False, column_name='place_id')
    place = TextField(null=False, column_name='place')
    visit_now = TextField(null=False, column_name='visit_now')
    visit_future = TextField(null=False, column_name='visit_future')

    class Meta:
        table_name = 'ivent_statistic'


class UserStat(BaseModel):
    tg_id = TextField(null=False, column_name='tg_id')
    name = TextField(null=True, column_name='name')
    phone = TextField(null=True, column_name='phone')
    visit_now = TextField(null=False, column_name='visit_now')
    visit_future = TextField(null=False, column_name='visit_future')

    class Meta:
        table_name = 'user_stat'


try:
    IventStatistic.create_table()
    UserStat.create_table()
except:
    pass