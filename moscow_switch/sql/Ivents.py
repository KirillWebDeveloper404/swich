from peewee import *
from .BaseModel import BaseModel


class Who(BaseModel):

    name = TextField(column_name='name')

    def __str__(self) -> str:
        return self.name
    
    class Meta:

        db_table = 'who'
        managed = True


class Kategory(BaseModel):

    name = TextField(column_name='name')
    desc = TextField(column_name='desc')
    for_who = ForeignKeyField(Who)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'kategory'
        managed = True


class PlacesGroup(BaseModel):

    name = TextField(column_name='name')
    kategory = ForeignKeyField(Kategory)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'plases_group'
        managed = True


class Place(BaseModel):

    name = TextField(column_name='name')
    desc = TextField(column_name='desc')
    group = ForeignKeyField(PlacesGroup)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'places'
        managed = True


class ActPlace(BaseModel):

    name = TextField(column_name='name')
    desc = TextField(column_name='desc')

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'act_places'
        managed = True


class IventItem(BaseModel):

    place = ForeignKeyField(ActPlace)
    users = TextField(column_name='users')

    class Meta:
        db_table = 'iventitems'
        managed = True

try:
    IventItem.create_table()
except:
    pass