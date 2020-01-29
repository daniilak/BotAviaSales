# /usr/bin/env python3.7
# -*- coding: utf-8 -*-

from peewee import *
import peewee
import datetime
from lib.BaseModel import BaseModel

class Aviasales_subs(BaseModel):
    id = PrimaryKeyField(null=False)
    user_id = IntegerField(null=False, default=0)
    type_sub = IntegerField(null=False, default=0)
    type_sales = IntegerField(null=False, default=0)
    depart_date = DateTimeField(default=datetime.datetime.now())
    return_date = DateTimeField(default=datetime.datetime.now())
    origin = TextField(null=False, default='')
    destination = TextField(null=False, default='')
    count_men = IntegerField(null=False, default=1)

class Meta:
    db_table = "aviasales_subs"
    order_by = ('id',)



def add_subs(user_id, type_sub, origin, count_days, tmp_dates_from):
    if len(tmp_dates_from) == 0:
        return False
    for date in tmp_dates_from.split("%"):
        if len(date) > 0:
            d_0, d_1, d_2 = date.split("_")
            if len(d_1) == 0:
                d_1 = "0" + d_1
            if len(d_2) == 0:
                d_2 = "0" + d_2
            depart_date = "2020-" + d_1 + "-" + d_2
            d = date.split("_")[1]
            if len(d) == 0:
                d = "0" + d
            row = Aviasales_subs(
                user_id=user_id,
                type_sub=type_sub,
                type_sales=type_sub,
                depart_date=depart_date,
                count_days=count_days,
                origin=origin.strip(),
            )
            row.save(force_insert=True)


def try_subs_by_user_id(user_id):
    try:
        return Aviasales_subs.select().where(Aviasales_subs.user_id == int(user_id))
    except Aviasales_subs.DoesNotExist:
        return False

def try_subs(user_id):
    try:
        return Aviasales_subs.select().where(Aviasales_subs.id == int(id)).get()
    except Aviasales_subs.DoesNotExist:
        return False


def find_subs(id):
    subs = try_subs(id)
    if not subs:
        return False
    return subs

def get_subs():
    try:
        return Aviasales_subs.select(fn.date_add(Aviasales_subs.depart_date, NodeList((SQL('INTERVAL'), Aviasales_subs.count_days, SQL('DAY')))), Aviasales_subs.user_id, Aviasales_subs.depart_date, Aviasales_subs.depart_date, Aviasales_subs.origin)
    except Aviasales_subs.DoesNotExist:
        return False
