#coding=utf-8
from Core.BaseCase import BaseCase

class LanguageCase(BaseCase):
    """
    Language表检查 1、id不能重复
    """
    def run(self):
        self.add_depends('Language')
        Language = self._Language
        self.tag_repeat(Language,'id')