#!/usr/bin/python3
#coding=utf-8
'''
libiqi 20220124 新增main_svn，只检查 有变化的配表 和 没检查过的配表
'''
# from apscheduler.schedulers.blocking import BlockingScheduler
import time
from Core.Container import Container
from Core.Loader import Loader
from Core.SvnRecord import  SvnRecord
import os
import json
import Core.Logger as logger

def get_root():
    current_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_path, "config.json")
    with open(config_path, "r") as f:
        content = f.read()
        config_json = json.loads(content)
        return config_json

def write_json(config_json):
    current_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_path, "config.json")
    with open(config_path, "w") as f:
        json.dump(config_json,f)
        f.close()

def init():
    config_json = get_root()
    start = time.time()
    config_root = config_json["config_root"]
    report_root = config_json["report_root"]
    res_root = config_json["res_root"]
    Container.set_config("report_root", report_root)
    # Container.set_config("res_root", res_root)
    loader = Loader(config_root)
    Container.set_loader(loader)

def main():
    init()
    Container.merge_translate()
    Container.merge_reward()
    start = time.time()
    print("cost:", time.time() - start)
    project_root = os.path.dirname(os.path.abspath(__file__))
    case_root = os.path.join(project_root, "Cases")
    # Container.test_one("Battle", "TestCase9")
    case_data = Container.run_case(case_root)
    Container.print_report(case_data)
    # Container.print_check()
    print("cost:", time.time() - start)

def check_self():
    init()
    config_root = "/Users/topjoy/data/vega/config/config"
    loader = Loader(config_root)
    loader.load_all()
    Container.print_check()

def test(category, clss):
    init()
    Container.merge_translate()
    Container.merge_reward()
    # start = time.time()
    # print("cost:", time.time() - start)
    Container.test_one(category, clss) 
    # print("cost:", time.time() - start)

def main_svn():
    init()
    Container.merge_translate()
    # Container.merge_reward()
    config_json = get_root()
    svn_root     = config_json["svn_root"]
    config_root  = config_json["config_root"]
    not_check    = config_json["not_check"]
    svn_reverson = config_json["svn_reverson"]
    svn_config = SvnRecord(svn_root)
    svn_config.get_reverson()
    if svn_config._reverson_now == svn_reverson:
        print('没人提交')
        return
    # os.system('svn update '+ svn_root)
    svn_config.set_last_check_reverson(svn_reverson)
    svn_config.set_not_check(not_check)
    not_check = []
    file = svn_config.change_file(config_root)
    for i in file:
        try:
            Container.test_one("DreamerCase",os.path.splitext(i)[0]+'Case')
        except:
            # logger.flyBook('没有{0}表的检查用例'.format(i)) # <at user_id="ou_xxx">用户名</at>
            not_check.append(i)
        if Container.need_recheck:
            not_check.append(i)
    config_json["svn_reverson"] = svn_config._reverson_now
    config_json["not_check"] = list(set(not_check))
    write_json(config_json)

if __name__ == "__main__":
    main_svn()
    # scheduler = BlockingScheduler()
    # scheduler.add_job(main_svn,'interval', seconds = 10)
    # scheduler.start()
    # test("Arena", "ArenaRobotCase")
    # main()
    # check_self()