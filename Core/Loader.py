#!/usr/bin/python3
#coding=utf-8

from Core.Container import Container
from Core.DreamerExcel import DreamerExcel
import threading
import os

class load_thread(threading.Thread):
    def __init__(self, table_name, path):
        threading.Thread.__init__(self)
        self._path = path
        self._table_name = table_name

    def run(self):
        print("load-thread:", threading.current_thread().name, self._table_name)
        excel_obj = DreamerExcel(self._table_name, self._path)
        excel_obj.check_link()
        Container.pool[self._table_name] = excel_obj

EXCEL_SUFFIX = ".xlsx"
class Loader:
    def __init__(self, config_root):
        if not os.path.exists(config_root):
            raise Exception("[{}] is not a directory".format(config_root))
        self._config_root = config_root

    def load_all(self):
        self.load_with_path(self._config_root)

    def load_with_path(self, path, files=None):
        if not os.path.exists(path):
            raise Exception("{} is not a directory".format(path))
        thread_list = []
        if files == None:
            files = os.listdir(path)
        for f in files:
            table_name, ext = os.path.splitext(f)
            if ext == EXCEL_SUFFIX:
                t = load_thread(table_name, os.path.join(path, f))
                thread_list.append(t)
                t.start()
        for t in thread_list:
            t.join()

    def load_batch(self, table_name_list):
        new_files = [ t + EXCEL_SUFFIX for t in table_name_list]
        self.load_with_path(self._config_root, new_files)

    def load_match(self, match_rule):
        files = os.listdir(self._config_root)
        new_files = [t for t in files if t.find(match_rule) == 0 ]
        self.load_with_path(self._config_root, new_files)

    def load_one(self, table_name):
        path = os.path.join(self._config_root, table_name + EXCEL_SUFFIX)
        excel_obj = DreamerExcel(table_name, path)
        excel_obj.check_link()
        Container.pool[table_name] = excel_obj
        return excel_obj



