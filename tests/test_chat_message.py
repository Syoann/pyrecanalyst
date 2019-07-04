import os
import sys
import unittest

from pyrecanalyst.Model.ChatMessage import ChatMessage


class TestChatMessage(unittest.TestCase):
    def test_init(self):
        msg = ChatMessage()
        self.assertEqual(msg.time, 0)
        self.assertEqual(msg.player, None)
        self.assertEqual(msg.msg, '')
        self.assertEqual(msg.group, '')

    def test_create_std(self):
        raw = "<All>Papain: Donnez moi vos excedents"
        msg = ChatMessage.create(1526, None, raw)
        self.assertEqual(msg.msg, "Donnez moi vos excedents")
        self.assertEqual(msg.group, "All")
        self.assertEqual(msg.player.name, "Papain")

    def test_create_voobly(self):
        raw = "<Rating> PlayerName: message"
        msg = ChatMessage.create(1526, None, raw)
        self.assertEqual(msg.msg, "message")
        self.assertEqual(msg.group, "Rating")
        self.assertEqual(msg.player.name, "PlayerName")
        self.assertEqual(msg.time, 1526)

