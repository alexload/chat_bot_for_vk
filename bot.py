# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import logging

try:
    import settings
except ImportError:
    exit('do cp settings.py.default settings.py and set token')

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

log = logging.getLogger('bot')
def loging_for_bot():
    handler = logging.StreamHandler()
    handler.setLevel(level=logging.DEBUG)
    handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    log.addHandler(handler)

    file_handler = logging.FileHandler(filename='bot.log', mode='a', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    file_handler.setLevel(logging.ERROR)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)

class BotVk:
    """
    Bot for vk.com
    """

    def __init__(self, group_id, token):
        """

        :param group_id: group id for vk.com
        :param token: token for group in vk.com
        """
        self.group_id = group_id
        self.token = token

        self.vk = vk_api.VkApi(token=self.token)
        self.bot_long_poller = VkBotLongPoll(vk=self.vk, group_id=self.group_id)
        self.api_vk = self.vk.get_api()

    def run(self):
        """
        Run bot
        :return: None
        """
        for event in self.bot_long_poller.listen():
            try:
                log.info('получено новое событие')
                self._on_event(event=event)
            except Exception:
                log.exception('получена ошибка')

    def _on_event(self, event):
        """
        Handles param: event
        :param event:   object class VkBotMessageEvent
        :return: None
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.info('отсылаем сообщение пользователю назад')
            self.api_vk.messages.send(peer_id=event.object.peer_id,
                                      message=event.object.text,
                                      random_id=random.randint(1, 2 ** 30),
                                      )
        else:
            log.error('ошибка типа type')


if __name__ == '__main__':
    loging_for_bot()
    bot = BotVk(group_id=settings.GROUP_ID, token=settings.TOKEN    )
    bot.run()
