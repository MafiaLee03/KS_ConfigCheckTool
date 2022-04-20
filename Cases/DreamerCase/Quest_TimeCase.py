#coding=utf-8
from Core.BaseCase import BaseCase

class Quest_TimeCase(BaseCase):
    """
    Quest_Time表检查 1、id不能重复 2、描述在language能找到
    """
    def run(self):
        self.add_depends('Quest_Time')
        Quest_Time = self._Quest_Time
        self.add_depends('Language')
        Language = self._Language
        self.tag_repeat(Quest_Time,'id')
        self.a_in_b(Quest_Time,Language,'des')
        self.a_in_b(Quest_Time,Language,'openDes')