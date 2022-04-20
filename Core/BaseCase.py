#coding=utf-8
from multiprocessing.sharedctypes import Value
from Core.Container import Container
from collections import Counter
from Core.Logger import *
import os
from Core.Util import *
class BaseCase:
    def __init__(self, name, category):
        self.title = "" # 用于测试报告展示
        self.desc = "" # 用于测试报告展示
        self._error_detail = []
        self._correct_cnt = 0
        self._error_cnt = 0
        self._success = True
        self._level = 1 #TODO 这里做枚举，用于区分用例的级别
        self._name = name
        self._category = category
        self._fail_case = False
        self._fb_error_detail = [self._name[:-4] + '表：'+'\n'] # 储存当前表的报错信息
        self._too_much_error = False
        self._max_fbreport_error = 50 # 一个表错误超出这个值就不再报出了

    def add_depends(self, table_name):
        table_obj = Container.find_table(table_name)
        alias_name = table_name.replace(".", "_")
        setattr(self, "_" + alias_name, table_obj)

    def run(self):
        pass
    
    def flybook_assert(self,is_correct,msg):
        if is_correct:
            self._correct_cnt = self._correct_cnt + 1
        else:
            self._error_cnt = self._error_cnt + 1
            if self._too_much_error: # 报错太多后面的就不报了
                return
            self._success = False
            self._fail_case = True
            if msg+'\n' not in self._fb_error_detail: # 去除重复错误
                self._fb_error_detail.append(msg+'\n')
            if len(self._fb_error_detail) > self._max_fbreport_error:
                self._too_much_error = True
                self._fb_error_detail.append('………………\n'+self._name + '表错误过多，请检查'+'\n')

    def get_fail_case(self):
        return self._fail_case

    def do_assert(self, is_correct, msg, record, comment=None):
        if is_correct:
            self._correct_cnt = self._correct_cnt + 1
        else:
            self._error_cnt = self._error_cnt + 1
            self._success = False
            tag = ""
            if type(record) == str:
                tag = record
            else:
                tag = record.tag
            self._error_detail.append([tag, msg, comment])
    
    def is_success(self):
        return self._success
    
    def convert_list_to_html(self, value_list):
        if len(value_list) <= 0:
            return ""
        html = []
        html.append("<html><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/><body>")
        html.append("<h1>")
        html.append("{}/{}".format(self._category,self._name))
        html.append("</h1>")
        html.append("<h3>")
        html.append(self.title)
        html.append("</h3>")
        html.append("<p>")
        html.append(self.desc)
        html.append("</p>")
        head_list = ["Tag", "错误描述", "备注"]
        table_html = convert_list_to_table(head_list, value_list)
        html.extend(table_html)
        html.append("</html>")
        return "".join(html)

    def dump_detail_report(self, report_root):
        report_path = os.path.join(report_root, self._category,"{}.html".format(self._name))
        report_dir = os.path.dirname(report_path)
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        with open(report_path, 'w', encoding="utf-8") as f:
            f.write(self.convert_list_to_html(self._error_detail))

    def get_summary(self):
        return [self._name, self.title, self.desc, self._correct_cnt, self._error_cnt]

##############################################################################################
###################################检查方法####################################################
##############################################################################################

    def tag_repeat(self,table_obj,key):
        '''
        输入表和key检查key列的值是否有重复
        '''
        name = table_obj._table_name
        list_key = []
        for record in table_obj.get_records():
            i = record._dict[key]
            list_key.append(i)
        dict_key = dict(Counter(list_key))
        value = [key for key,value in dict_key.items() if value > 1]
        if value != []:
            str_value = str(value)[1:-1] # 去掉括号
            self.flybook_assert(0,'{0}列有重复值:{1}'.format(key,str_value))

    def a_in_b(self,table_obj_a,table_obj_b,keya:str|tuple|list,keyb:str|tuple|list = 'id',va = 0,vb = 0):
        '''
        检查表A的某列值是否被表B某列值包含
        table_obj_a ：表A
        table_obj_b ：表B
        keya        ：A表的哪列值 支持值为多维数组，会遍历取所有值的[va]
        keyb        ：B表的哪列值 默认为id
        va          ：keya的下标 默认0 如果写-1则检查list中所有
        vb          ：keyb的下标 默认0
        '''
        namea = table_obj_a._table_name
        nameb = table_obj_b._table_name
        table_obj_b = Container.find_table(nameb)
        list_key_b = []
        for record in table_obj_b.get_records():
            if isinstance(keyb,str):
                i = record._dict[keyb]
                if type(i) != list:
                    list_key_b.append(str(i))
                else:
                    list_key_b.append(str(i[vb]))
            elif isinstance(keyb,(tuple,list)):
                for k in keyb:
                    list_key_b.append(str(record._dict[k]))
            else:
                raise TypeError('keyb must be a str,tuple or list!')
        for record in table_obj_a.get_records():
            if isinstance(keya,str):
                id_a = record.id
                i = record._dict[keya]
                self.func_a_in_b(i,list_key_b,keya,nameb,keyb,va)
            elif isinstance(keya,(tuple,list)):
                id_a = record.id
                for k in keya:
                    i = record._dict[k]
                    self.func_a_in_b(i,list_key_b,keya,nameb,keyb,va)

    def func_a_in_b(self,i,list_key_b,keya,nameb,keyb,va): # 用于辅助a_in_b的函数
        if type(i[0]) == list:
            for j in i:
                self.func_a_in_b(j,list_key_b,keya,nameb,keyb,va)
            return
        if type(i) != list:
            i = str(i)
            self.flybook_assert(i in list_key_b,'{0}配置错误,在{1}表{2}列找不到 值：{3}'.format(keya,nameb,keyb,i))
        elif va == -1:
            for check_value in i:
                self.flybook_assert(check_value in list_key_b,'{0}配置错误,在{1}表{2}列找不到 值：{3}'.format(keya,nameb,keyb,i))
        else:
            i = str(i[va])
            self.flybook_assert(i in list_key_b,'{0}配置错误,在{1}表{2}列找不到 值：{3}'.format(keya,nameb,keyb,i))        

    def value_in_b(self,key,table_obj_b,value:str|tuple|list,keyb:str|tuple|list = 'id',value_real = None,vb = 0):
        '''
        检查某值是否被表B某列值包含
        key         ：判断值的tag，只用作出错后的提示
        table_obj_b ：表B
        value       ：判断值
        keyb        ：B表的哪列值 默认为id
        value_real  ：判断值在key列内的真实value，用于出错后的提示
        vb          ：keyb的下标 默认0
        '''
        if value_real == None:
            value_real = value
        nameb = table_obj_b._table_name
        table_obj_b = Container.find_table(nameb)
        list_key_b = []
        for record in table_obj_b.get_records():
            if isinstance(keyb,str):
                i = record._dict[keyb]
                if type(i) != list:
                    list_key_b.append(str(i))
                else:
                    list_key_b.append(str(i[vb]))
            elif isinstance(keyb,(tuple,list)):
                for k in keyb:
                    list_key_b.append(str(record._dict[k]))
            else:
                raise TypeError('keyb must be a str,tuple or list!')
        if isinstance(value,str):
            self.flybook_assert(value in list_key_b,'{0}配置错误,{1}在{2}表{3}列找不到 值：{4}'.format(key,value,nameb,keyb,value_real))
        elif isinstance(value,(tuple,list)):
            for k in value:
                self.flybook_assert(str(k) in list_key_b,'{0}配置错误,{1}在{2}表{3}列找不到 值：{4}'.format(key,k,nameb,keyb,value_real))

    def rank_check(self,table_obj,key):
        '''
        排名类配表检查，检查内容：1、排名区间左不能大于右 2、排名区间无重合或缝隙
        '''
        name = table_obj._table_name
        rank_list = []
        for record in table_obj.get_records():
            i = record.id
            rank = record._dict[key]
            rank_list.append(rank)
            self.flybook_assert(rank[0]<=rank[1],'{0}区间错误，左大于右了 值：{1} id：{2}'.format(key,rank,i))
        rank_list = sorted(rank_list,key = lambda x:x[0])
        for i in range(len(rank_list) - 1):
            if rank_list[i][1] + 1 < rank_list[i+1][0]:
                self.flybook_assert(0,'{2}列排名区间有缝隙，可能出现某名次不落在任何区间 区间：{0} {1}'.format(rank_list[i],rank_list[i+1],key))
            elif rank_list[i][1] + 1 > rank_list[i+1][0]:
                self.flybook_assert(0,'{2}列排名区间有重合 重合区间：{0} {1}'.format(rank_list[i],rank_list[i+1],key))