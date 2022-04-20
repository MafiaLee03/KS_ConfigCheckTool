#coding=utf-8
from Core.BaseCase import BaseCase
import threading

class ItemCase(BaseCase):
    """
    Item表配置检查，详情见用例配置检查页签
    """
    def run(self):
        self.add_depends('Item')
        Item = self._Item
        self.add_depends('Random_Chest')
        Random_Chest = self._Random_Chest
        self.add_depends('Gacha_Race')
        Gacha_Race = self._Gacha_Race
        self.tag_repeat(Item,'id')
        self.add_depends('Language')
        Language = self._Language
        # self.a_in_b(Item,Language,('name','des','typeName'))
        # t1 = threading.Thread(target=self.a_in_b,args=(Item,Language,'name'))
        # t2 = threading.Thread(target=self.a_in_b,args=(Item,Language,'des'))
        # t3 = threading.Thread(target=self.a_in_b,args=(Item,Language,'typeName'))
        self.a_in_b(Item,Language,'name')
        self.a_in_b(Item,Language,'des')
        self.a_in_b(Item,Language,'typeName')
        # thread_list = [t1,t2,t3]
        # for t in thread_list:
        #     t.start()
        # for t in thread_list:
        #     t.join()

        infoTypeList = ['1','2','3','4','5','6','7','10','None']
        useTypeList = ['1','2','3','4','5']
        for record in Item.get_records():
            i = record.id
            canUse = record.canUse
            useNeed = str(record.useNeed)
            infoType = str(record.infoType)
            useType = str(record.useType)
            prompt = str(record.prompt)
            useEff = record.useEff
            self.flybook_assert(infoType in infoTypeList,'Item表infoType填写错误，未找到类型 id：{0} 错误值：{1}'.format(i,infoType))
            if canUse == 1:
                self.flybook_assert(useType in useTypeList,'Item表useType填写错误，未找到类型 id：{0} 错误值：{1}'.format(i,useType))
                self.flybook_assert(useNeed != '0' and useNeed != 'None','Item表的useNeed填写错误,可用道具useNeed不应为0或空 id：{0} 错误值：{1}'.format(i,useNeed))
            else:
                self.flybook_assert(prompt != '1','Item表prompt配置错误，不可用道具不应配置红点 id：{0} 错误值：{1}'.format(i,prompt))
            if infoType in ['1','6','7']:
                self.flybook_assert(useType == 'None','Item表useType填写错误，infoType={1}，useType应为空 id：{0} 错误值：{2}'.format(i,infoType,useType))
            elif infoType == '2':
                self.flybook_assert(useType != '4' and useType != '5','Item表useType填写错误，infoType=2，useType不能为{1} id：{0} 错误值：{1}'.format(i,useType))
            elif infoType == '3':
                self.flybook_assert(useType == '1','Item表useType填写错误，infoType=3，useType不能为{1} id：{0} 错误值：{1}'.format(i,useType))
            elif infoType == '4':
                self.flybook_assert(useType == '2','Item表useType填写错误，infoType=4，useType不能为{1} id：{0} 错误值：{1}'.format(i,useType))
            elif infoType == '5':
                self.flybook_assert(useType == '4','Item表useType填写错误，infoType=5，useType不能为{1}  id：{0}错误值：{1}'.format(i,useType))
            elif infoType == '10':
                self.flybook_assert(useType == '5','Item表useType填写错误，infoType=10，useType不能为{1} id：{0} 错误值：{1}'.format(i,useType))
            if useType == '2':
                self.value_in_b('useEff',Random_Chest,str(useEff))
            elif useType == '3':
                useE3 = useEff.replace('[','').replace(']','')
                useE3 = useE3.split(',')
                for j in filter(lambda x:x%2==1,range(len(useE3))):
                    self.value_in_b('useEff',Gacha_Race,str(useE3[j]),value_real=useEff)