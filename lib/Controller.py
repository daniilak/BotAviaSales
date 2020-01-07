# /usr/bin/env python3.7
# -*- coding: utf-8 -*-
import json
import calendar
from lib.User import add_user, try_user, find_user
from lib.Subs import add_subs, try_subs_by_user_id, try_subs, find_subs
from lib.Requests import Requests

keyboard = json.dumps({
    "one_time": False,
    "buttons": [
        [{"action": {"type": "text",
                             "payload": "{\"button\": \"my_subs\"}", "label": "Мои подписки"}}],
        [{"action": {"type": "text", "payload": "{\"button\": \"add_subs\"}",
                             "label": "Добавить подписку"}}]
    ]
})
k_null = json.dumps({"one_time": False, "buttons": []})

k_type = json.dumps({
    "one_time": False,
    "buttons": [
        [{"action": {"type": "text", "payload": "{\"button\": \"all\"}",
                             "label": "Все"}}],
        [{"action": {"type": "text",
                             "payload": "{\"button\": \"avia\"}", "label": "Авиа"}}],
        # [{"action": {"type": "text", "payload": "{\"button\": \"turs\"}",
        #                      "label": "Туры (not work)"}}],
        # [{"action": {"type": "text", "payload": "{\"button\": \"bus\"}",
        #                      "label": "Автобусы (not work)"}}],
        # [{"action": {"type": "text", "payload": "{\"button\": \"hostel\"}",
        #                      "label": "Отели (not work)"}}],
        [{"action": {"type": "text", "payload": "{\"button\": \"back\"}",
                             "label": "В главное меню"}}]
    ]
})

class Controller:
    def __init__(self, update_object):
        print("Controller init")
        self.u = update_object

        self.user = find_user(update_object['from_id'])
        self.text = update_object['text']
        print(self.user.level, self.user.id)

        self.command = self.payloadParse()
        self.r = Requests(update_object['peer_id'])
        self.payloadParse()

        self.switchLevel(self.user.level)

    def starting(self):
        if not self.command:
            self.r.send_msg(
                "Добро пожаловать в чат-бота уведомлений по ценам, управление кнопками!", keyboard)
        if self.command == "start":
            self.r.send_msg(
                "Добро пожаловать в чат-бота уведомлений по ценам, управление кнопками!", keyboard)
            return
        if self.command == "my_subs":
            subs = try_subs_by_user_id(self.user.id)
            if not subs:
                self.r.send_msg("У вас ничего нет", keyboard)
                return
            msg = "Ваши подписки: \n"
            for sub in subs:
                msg += "{0}\n".format(sub.id)
            self.r.send_msg(msg, keyboard)
            return
        if self.command == "add_subs":
            self.r.send_msg("Выберите тип", k_type)
            self.user.level = 1
            self.user.save()
            return

        self.r.send_msg(
            "Добро пожаловать в чат-бота уведомлений по ценам, управление кнопками!", keyboard)
        return

    def isBack(self):
        if self.command == "back":
            self.user.level = 0
            self.user.save()
            self.switchLevel(0)
            return True
        return False

    def adding(self):
        if self.isBack():
            return
            # надо сохранить во временную, лучше в поле таблицы User
        self.user.level = 2
        self.user.tmp_type = self.command
        self.user.save()
        self.r.send_msg(
            "Сохранено. Введите город отправления", k_null)
        self.switchLevel(2)

    def city(self):
        if self.isBack():
            return
        # Проверка города
        self.user.level = 3
        self.user.tmp_city = self.text
        self.user.save()
        # Лушче сделать календарь (отметьте)
        self.r.send_msg(
            "Не сохранили, но выбрано. Введите даты отправления", self.monthRender())
        self.switchLevel(3)

    def dateFrom(self):
        if self.isBack():
            return
        # если нажата сохранить
        if self.command == "go_month":
            self.r.send_msg("Вернулись к месяцам", self.monthRender())
            return True
        if self.command == "save":
            self.user.level = 4
            self.user.save()
            self.switchLevel(4)
            self.r.send_msg("Не сохранили, но выбрано. Введите дату домой в формате ГГГГ-ММ-ДД", k_null)
            return True
        splitted = self.command.split("_")
        print(splitted)
        if splitted[0] == "mon":
            self.r.send_msg("*Выбран месяц #{0}*".format(splitted[1]), self.daysRender(splitted[1]))
        if splitted[0] == "day":
            if splitted[1] == "X":
                self.r.send_msg("Так низя", self.daysRender(splitted[2]))
                return True
            label = False
            if len(self.user.tmp_dates_from) > 0:
                for date in self.user.tmp_dates_from.split("%"):
                    if date.split("_")[1] == splitted[2] and date.split("_")[2] == splitted[1]:
                        label = True
                self.user.tmp_dates_from = self.user.tmp_dates_from + "%"

            if not label:
                self.user.tmp_dates_from = self.user.tmp_dates_from  + "2020_{0}_{1}".format(splitted[2],splitted[1])
                self.r.send_msg("*Выбран день #{0}*".format(splitted[1]), self.daysRender(splitted[2]))
            else:
                label = ""
                for date in self.user.tmp_dates_from.split("%"):
                    if len(date) > 0:
                        if date.split("_")[1] == splitted[2] and date.split("_")[2] == splitted[1]:
                            label = label
                        else:
                            label = label + date + "%"
                self.user.tmp_dates_from = label[0:-1]
                self.r.send_msg("*Убран день #{0}*".format(splitted[1]), self.daysRender(splitted[2]))
            self.user.save()


    def dateTo(self):
        if self.isBack():
            return
        # Проверка даты
        self.user.level = 0
        self.user.save()
        self.r.send_msg("ВСЁ ТИПА СОХРАНЕНО", k_null)
        # save to bd
        self.switchLevel(0)

    def switchLevel(self, level):
        if level == 0:
            self.starting()
        if level == 1:
            self.adding()
        if level == 2:
            self.city()
        if level == 3:
            self.dateFrom()
        if level == 4:
            self.dateTo()

    def payloadParse(self):
        if self.u.get('payload'):
            a = json.loads(self.u['payload'], strict=False, encoding='utf-8')
            if a.get('button') and len(a['button']) > 0:
                return a['button']
        return False

    def monthRender(self):
        month = [["Январь", "Февраль", "Март"], ["Апрель", "Май", "Июнь"], ["Июль", "Август", "Сентябрь"], ["Октябрь", "Ноябрь", "Декабрь"]]
        k_month = {"one_time": False, "buttons": []}
        i = 0
        for mon in month:
            buttons = []
            for m in mon:
                buttons.append({"action": {"type": "text", "payload": "{\"button\": \"mon_" + str(i) + "\"}", "label": m}, "color": "secondary"})
                i += 1
            k_month['buttons'].append(buttons)
        k_month['buttons'].append([{"action": {"type": "text", "payload": "{\"button\": \"save\"}", "label": "Сохранить"}, "color": "positive"}])
        return json.dumps(k_month)
    
    def daysRender(self, monthId):
        kDays = {"one_time": False, "buttons": []}
        c = calendar.TextCalendar(calendar.MONDAY)
        s = c.monthdayscalendar(2020, int(monthId) + 1)
        for x in zip(*s): 
            buttons = []
            for i in x: 
                label = "secondary"
                if (i == 0):
                    i = "X"
                else:
                    if len(self.user.tmp_dates_from) > 0:
                        for date in self.user.tmp_dates_from.split("%"):
                            if date.split("_")[1] == monthId and date.split("_")[2] == str(i):
                                label = "positive"
                buttons.append({"action": {"type": "text", "payload": "{\"button\": \"day_" + str(i) + "_"+str(monthId)+"\"}", "label": i}, "color": label})
            kDays['buttons'].append(buttons)
        kDays['buttons'].append([{"action": {"type": "text", "payload": "{\"button\": \"go_month\"}", "label": "К месяцам"}, "color": "primary"}])
        kDays['buttons'].append([{"action": {"type": "text", "payload": "{\"button\": \"save\"}", "label": "Сохранить"}, "color": "positive"}])
        return json.dumps(kDays)
