from django.db import models


class IventStatistic(models.Model):
    place_id = models.TextField(null=False, verbose_name='place_id')
    place = models.TextField(null=False, verbose_name='Название')
    visit_now = models.TextField(null=False, verbose_name='Уже посетили')
    visit_future = models.TextField(null=False, verbose_name='Собираются посетить')

    class Meta:
        db_table = 'ivent_statistic'
        managed = True
        verbose_name = 'Ivent statistics'
        verbose_name_plural = 'Ivent statistic'


class UserStat(models.Model):
    tg_id = models.TextField(null=False, verbose_name='Телеграм id')
    name = models.TextField(null=True, verbose_name='Имя')
    phone = models.TextField(null=True, verbose_name='Телефон')
    visit_now = models.TextField(null=False, verbose_name='Уже посетил')
    visit_future = models.TextField(null=False, verbose_name='Собирается посетить')

    class Meta:
        db_table = 'user_stat'
        managed = True
        verbose_name = 'User statistics'
        verbose_name_plural = 'User statistic'
