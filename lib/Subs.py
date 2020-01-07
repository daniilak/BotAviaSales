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


def add_subs(user_id, type_sub, type_sales, depart_date, return_date, origin, destination):
    row = Aviasales_subs(
        user_id=user_id,
        type_sub=type_sub,
        type_sales=type_sales,
        depart_date=depart_date,
        return_date=return_date,
        origin=origin.strip(),
        destination=destination.strip(),
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
