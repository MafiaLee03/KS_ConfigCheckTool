#coding=utf-8
from Core.BaseCase import BaseCase

class Arena_RobotCase(BaseCase):
    """
    Arena_Robot表检查 1、id不能重复 2、rank不能重复 3、name在Language能找到
    """
    def run(self):
        self.add_depends('Arena_Robot')
        Arena_Robot = self._Arena_Robot
        self.add_depends('Language')
        Language = self._Language
        self.tag_repeat(Arena_Robot,'id')
        self.tag_repeat(Arena_Robot,'rank')
        self.a_in_b(Arena_Robot,Language,'name')