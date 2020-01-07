# /usr/bin/env python3.7
# -*- coding: utf-8 -*-
import re
import requests
import vk_api
from config import GROUP_ID, VK_API_ACCESS_TOKEN, VK_API_VERSION
from random import randint


class Requests:
    peer_id = 0

    def __init__(self, peer_id):
        print("Requests init")
        self.peer_id = peer_id
        vk_session = vk_api.VkApi(token=VK_API_ACCESS_TOKEN)
        self.api = vk_session.get_api()

    def api_full_name(self, user_id):
        name = self.api.users.get(user_ids=user_id)[0]
        return "{0} {1}".format(name['first_name'], name['last_name'])

    def send_msg(self, msg, keyboard):
        
        return self.api.messages.send (
            user_id=self.peer_id,
            random_id=randint(-2147483647, 2147483647),
            message=msg,
            keyboard=keyboard
        )
