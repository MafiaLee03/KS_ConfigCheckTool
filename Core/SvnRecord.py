#!/usr/bin/python3
#coding=utf-8
#author: libiqi

import subprocess
import re
import os

class SvnRecord:
    def __init__(self,url):
        self._url = url
        self._svn_log_last = ''
        self._last_check_reverson = 0
        self._reverson_now = 0
        self._not_check = []

    def get_svn_log_last(self):
        '''
        取svn最后一条提交记录
        '''
        self._svn_log_last = subprocess.getoutput('cd C:/Program Files/TortoiseSVN/bin&svn log -l1 '+ self._url)
    
    def get_reverson(self):
        '''
        返回最新的svn提交版本
        '''
        self.get_svn_log_last()
        self._reverson_now = re.search('(?<=r).*?(?= )',self._svn_log_last).group(0)
        # return re.search('(?<=r).*?(?= )',self._svn_log_last).group(0)

    def set_last_check_reverson(self,value):
        self._last_check_reverson = value

    def set_not_check(self,value):
        self._not_check = value

    def get_change_file(self,start,now):
        '''
        输入两个版本号，返回两个版本变化文件的list + 没写用例或其他导致之前没检查的表
        '''
        ver_str = subprocess.getoutput('cd C:/Program Files/TortoiseSVN/bin&svn log -r {0}:{1} -v {2}'.format(start,now,self._url))
        cha_list = re.findall('(?<=SVN).*?(?=\n)',ver_str)
        result = self._not_check
        for i in cha_list:
            filename = os.path.split(i)[1]
            result.append(filename)
            
        return set(result)
    def change_file(self,config_root):
        '''
        上次记录的版本到最新的svn提交之间变化的excel文件，如果没有返回全部excel文件
        '''
        file_list = []
        start = self._last_check_reverson
        self.get_reverson()
        reverson_now = self._reverson_now
        if start == reverson_now and start != 0:
            return self._not_check
        if start == 0 or start == '':
            file_list = os.listdir(config_root)
        else:
            file_list = self.get_change_file(start,reverson_now)
        # print(file_list)
        def check_xlse(str1):
            if os.path.splitext(str1)[1] == '.xlsx':
                return True
            return False
        result = filter(check_xlse,file_list)
        # print(list(result))
        return result