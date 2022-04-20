#coding=utf-8
from Core.BaseCase import BaseCase

class Data_SettingCase(BaseCase):
    """
    Data_Setting表检查 1、id不能重复
    """
    def run(self):
        self.add_depends('Data_Setting')
        Data_Setting = self._Data_Setting
        self.tag_repeat(Data_Setting,'id')