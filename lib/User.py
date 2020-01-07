# /usr/bin/env python3.7
# -*- coding: utf-8 -*-
import datetime
from peewee import PrimaryKeyField, TextField, IntegerField
from lib.BaseModel import BaseModel


class User(BaseModel):
    id = PrimaryKeyField(null=False)
    level = IntegerField(null=False, default=0)
    tmp_type = TextField(null=False, default="")
    tmp_city = TextField(null=False, default="")
    tmp_dates_from = TextField(null=False, default="")
    tmp_dates_to = TextField(null=False, default="")
    class Meta:
        db_table = "aviasales_users"
        order_by = ('id',)


def add_user(id):
    row = User(
        id=id
    )
    row.save(force_insert=True)


def try_user(id):
    try:
        return User.select().where(User.id == int(id)).get()
    except User.DoesNotExist:
        return False


def find_user(id):
    user = try_user(id)
    if not user:
        add_user(id)
        user = try_user(id)
    return user