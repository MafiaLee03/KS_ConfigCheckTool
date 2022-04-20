#coding=utf-8
from Core.BaseCase import BaseCase

class Arena_Reward_RankCase(BaseCase):
    """
    Arena_Reward_Rank表检查 1、id不能重复 2、排名区间不能左大于右,无缝隙或重合 3、奖励id要在item里能找到
    """
    def run(self):
        self.add_depends('Arena_Reward_Rank')
        self.add_depends('Item')
        Item = self._Item
        Arena_Reward_Rank = self._Arena_Reward_Rank
        self.tag_repeat(Arena_Reward_Rank,'id') #id不能重复
        self.a_in_b(Arena_Reward_Rank,Item,'reward','id',0) #奖励在item能找到
        self.a_in_b(Arena_Reward_Rank,Item,'seasonReward','id',0) #奖励在item能找到
        self.rank_check(Arena_Reward_Rank,'rank')