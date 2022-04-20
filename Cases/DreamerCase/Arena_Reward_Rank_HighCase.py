#coding=utf-8
from Core.BaseCase import BaseCase

class Arena_Reward_Rank_HighCase(BaseCase):
    """
    Arena_Reward_Rank_High表检查 1、id不能重复 2、排名区间不能左大于右 所有排名区间不能重合
    """
    def run(self):
        self.add_depends('Arena_Reward_Rank_High')
        Arena_Reward_Rank_High = self._Arena_Reward_Rank_High
        self.tag_repeat(Arena_Reward_Rank_High,'id')
        self.rank_check(Arena_Reward_Rank_High,'rank')