#coding=utf-8
from Core.BaseCase import BaseCase

class DemoCase(BaseCase):
    """
    注释，可以写这个用例检查了哪些点
    """
    def run(self):
        pass
        # self.add_depends('配表名')
        # 配表名 = self._配表名

        # 重复值检查 输入表和key检查key列的值是否有重复
        # self.tag_repeat(Language,'id')



        '''
        检查表A的某列值是否被表B某列值包含
        table_obj_a ：表A
        table_obj_b ：表B
        keya        ：A表的哪列值
        keyb        ：B表的哪列值 默认为id
        va          ：keya的下标 默认0 如果写-1则检查list中所有
        vb          ：keyb的下标 默认0
        '''
        # self.a_in_b(table_obj_a = 表A,table_obj_b = 表B,keya = '字段名A',keyb = 'id',va = 0,vb = 0)



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
