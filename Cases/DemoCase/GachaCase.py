#coding=utf-8
from Core.BaseCase import BaseCase

class GachaCase(BaseCase):
    """
    注释，可以写这个用例检查了哪些点
    """
    def run(self):
        pass
        self.add_depends('Gacha')
        Gacha = self._Gacha

        self.add_depends('Enu_Reward')
        Enu_Reward = self._Enu_Reward

        # 重复值检查 输入表和key检查key列的值是否有重复
        self.tag_repeat(Gacha,'id')
        self.tag_repeat(Gacha,'pool')



        '''
        检查表A的某列值是否被表B某列值包含
        table_obj_a ：表A
        table_obj_b ：表B
        keya        ：A表的哪列值
        keyb        ：B表的哪列值 默认为id
        va          ：keya的下标 默认0 如果写-1则检查list中所有
        vb          ：keyb的下标 默认0
        '''
        self.a_in_b(table_obj_a = Gacha,table_obj_b = Enu_Reward,keya = 'cost',keyb = 'id',va = 0,vb = 0)
        self.a_in_b(table_obj_a = Gacha,table_obj_b = Enu_Reward,keya = 'cost10',keyb = 'id',va = 0,vb = 0)
        for i in Gacha.get_records():
            displayP = i.displayP
            id = i.id
            if displayP == None:
                continue
            # 分别取出三个值
            value1 = displayP[0]
            value2 = displayP[1]
            value3 = displayP[2]

            # 去掉百分号
            value1 = value1[0:-1]
            value2 = value2[0:-1]
            value3 = value3[0:-1]

            # str转成float
            value1 = float(value1)
            value2 = float(value2)
            value3 = float(value3)
            self.flybook_assert(round(value1+value2+value3,4) == 100.0,'概率配置错误,加和应该等于1,错误id:{0}'.format(id))


        '''
        检查某值是否被表B某列值包含
        key         ：判断值的tag，只用作出错后的提示
        table_obj_b ：表B
        value       ：判断值
        keyb        ：B表的哪列值 默认为id
        value_real  ：判断值在key列内的真实value，用于出错后的提示
        vb          ：keyb的下标 默认0
        '''
        # self.value_in_b(key = 'tag名',table_obj_b = '表B',value = '要检查的某值',keyb = 'id',value_real = None,vb = 0)
