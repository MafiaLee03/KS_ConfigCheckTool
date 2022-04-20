from Core.BaseCase import BaseCase

class Arena_Robot_HighCase(BaseCase):
    """
    Arena_Robot_High表检查 1、id不能重复 2、rank不能重复 3、name在Language能找到
    """
    def run(self):
        self.add_depends('Arena_Robot_High')
        Arena_Robot_High = self._Arena_Robot_High
        self.add_depends('Language')
        Language = self._Language
        self.tag_repeat(Arena_Robot_High,'id')
        self.tag_repeat(Arena_Robot_High,'rank')
        self.a_in_b(Arena_Robot_High,Language,'name')