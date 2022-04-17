from unicodedata import name
from django.db import models


class User(models.Model):

    tg_id = models.TextField(null=False, verbose_name='tg_id')
    photo = models.TextField(null=True, verbose_name='Фото профиля')
    name = models.TextField(null=True, verbose_name='Имя')
    phone = models.TextField(null=True, verbose_name='Номер телефона')
    status = models.TextField(null=False, verbose_name='Статус')
    tarif = models.TextField(null=True, verbose_name='Тариф')
    dead_line = models.TextField(null=True, verbose_name='Дата окончания тарифа')

    lenght = models.TextField(null=True, verbose_name='Рост')
    weight = models.TextField(null=True, verbose_name='Вес')
    age = models.TextField(null=True, verbose_name='Возраст')
    ocupation = models.TextField(null=True, verbose_name='Вид деятельности')

    def __str__(self) -> str:
        return f'#{self.id} {self.name}'

    class Meta:
        
        db_table = 'users'
        managed = True
        verbose_name = 'users'
        verbose_name_plural = 'user'


class Admin(models.Model):
    tg_id = models.TextField(null=False, verbose_name='tg_id')

    def __str__(self) -> str:
        return self.tg_id

    class Meta:
        db_table = 'admins'
        managed = True
        verbose_name = 'Admins'
        verbose_name_plural = 'Admin'


class Who(models.Model):

    name = models.TextField(verbose_name='Название группы')

    def __str__(self) -> str:
        return self.name
    
    class Meta:

        db_table = 'who'
        managed = True
        verbose_name = 'who'
        verbose_name_plural = 'who'


class Kategory(models.Model):

    name = models.TextField(verbose_name='Название категории')
    desc = models.TextField(verbose_name='Описание')
    for_who = models.ForeignKey(Who, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'kategory'
        managed = True
        verbose_name = 'kategory'
        verbose_name_plural = 'kategorys'


class PlacesGroup(models.Model):

    name = models.TextField(verbose_name='Название группы мест')
    kategory = models.ForeignKey(Kategory, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'plases_group'
        managed = True
        verbose_name = 'places group'
        verbose_name_plural = 'places group'


class Place(models.Model):

    name = models.TextField(verbose_name='Название места/мероприятия')
    desc = models.TextField(verbose_name='Описание')
    group = models.ForeignKey(PlacesGroup, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'places'
        managed = True
        verbose_name = 'place'
        verbose_name_plural = 'places'


class ActPlace(models.Model):

    name = models.TextField(verbose_name='Название места/мероприятия')
    desc = models.TextField(verbose_name='Описание')

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = 'act_places'
        managed = True
        verbose_name = 'active place'
        verbose_name_plural = 'active places'


class ADS_db(models.Model):

    name = models.TextField(verbose_name='Имя')
    phone = models.TextField(verbose_name='Номер телефона')
    address = models.TextField(verbose_name='Адрес места')
    link = models.TextField(verbose_name='Ссылка на сайт')
    desc = models.TextField(verbose_name='Описание')

    class Meta:
        db_table = 'ads'
        managed = True
        verbose_name = 'ADS'
        verbose_name_plural = 'ADS'
