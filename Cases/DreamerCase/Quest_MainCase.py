#coding=utf-8
from Core.BaseCase import BaseCase

class Quest_MainCase(BaseCase):
    """
    Quest_Main表检查 1、id不能重复
    """
    def run(self):
        self.add_depends('Quest_Main')
        Quest_Main = self._Quest_Main
        self.tag_repeat(Quest_Main,'id')