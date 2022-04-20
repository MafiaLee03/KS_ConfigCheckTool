#!/usr/bin/python3
#coding=utf-8
class ExcelRecord:
    def __init__(self, excel_obj, data_dict):
        self._dict = data_dict
        self._excel_obj = excel_obj
    def __getattr__(self, key_name):
        link_obj = self._excel_obj.get_link_excel(key_name)
        if link_obj and link_obj._table_name == "Language":
            # Language 表需要特殊处理
            link_record = link_obj.get_record(self._dict.get(key_name))
            if link_record == None:
            # TODO 这种情况是没有配置 需要记录
                return None
            return link_record.text
        else:
            return self._dict.get(key_name)
    def get_value(self, key_name):
        return self._dict.get(key_name)

