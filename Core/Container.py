#!/usr/bin/python3
#coding=utf-8
import os
import importlib
import os
from Core.Util import *
from Core.Logger import logError

class Container:
    """
    所有的表对象都靠 Container来维护
    """
    table_name = ''
    pool = {}
    _config = {}
    exceptions = []
    _loader = None
    need_recheck = False
    _fail_msg = []

    @classmethod
    def set_loader(clz, loader):
        clz._loader = loader

    @classmethod
    def find_table(clz, table_name):
        config = clz.pool.get(table_name)
        if config == None:
            config = clz._loader.load_one(table_name)
        return config

    @classmethod
    def run_case(clz, case_root):
        report_root = clz.get_config("report_root")
        case_data = []
        categorys = [d for d in os.listdir(case_root) if d.find("__") < 0 and d.find(".") < 0]
        for category in categorys:
            p = os.path.join(report_root, category)
            case_list = [c[:-3] for c in os.listdir(os.path.join(case_root, category)) if c.find("Case") >=0]
            if not os.path.exists(p):
                os.makedirs(p)
            all_case = 0
            success_case = 0
            fail_case = 0
            category_data = []
            for case in case_list:
                clss = case
                try:
                    print("Cases.{}.{}".format(category, clss))
                    module = importlib.import_module("Cases.{}.{}".format(category, clss))
                except Exception as e:
                    break
                instance = module.__dict__[clss](clss, category)
                try:
                    instance.run()
                except Exception as e:
                    clz._fail_msg.append('\n{}用例运行错误:{}\n'.format(case,e))
                    clz._fail_msg.append('———————————————————\n')
                    logError('{}用例运行错误:{}'.format(case,e))
                if instance.is_success():
                    success_case = success_case + 1
                else:
                    fail_case = fail_case + 1
                    clz._fail_msg.extend(instance._fb_error_detail)
                    clz._fail_msg.append('———————————————————\n')
                category_data.append(instance.get_summary())
                instance.dump_detail_report(report_root)
            clz.print_category(report_root, category, category_data)
            all_case = success_case + fail_case
            case_data.append([category, all_case, success_case, fail_case])
        return case_data

    @classmethod
    def print_report(clz, case_data):
        html = []
        report_root = clz.get_config("report_root")
        html.append("<html><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/><body>")
        html.append("<h3>")
        html.append("测试报告")
        html.append("</h3>")
        head_list = ["分类", "总用例数", "执行成功", "执行失败"]
        table_html = convert_list_to_table(head_list, case_data)
        html.extend(table_html)
        html.append("<script>")
        html.append("var space = document.getElementsByTagName(\"th\").length - 1;")
        html.append("var td_list = document.getElementsByTagName(\"td\");")
        html.append("for(var i=space; i< td_list.length; i=i+space+1){")
        html.append("var c = td_list[i-space].innerText;")
        html.append("td_list[i].innerHTML='<a href=\"' + c + '/' + c + '.html\">' + td_list[i].innerText +  '</a>'; ")
        html.append("}")
        html.append("</script>")
        html.append("</html>")
        report_path = os.path.join(report_root, "report.html")
        content = " ".join(html)
        with open(report_path, 'w', encoding="utf-8") as f:
            f.write(content)

    @classmethod
    def print_category(clz, report_root, categroy, category_data):
        html = []
        html.append("<html><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/><body>")
        html.append("<h3>")
        html.append("{}用例详细".format(categroy))
        html.append("</h3>")
        head_list = ["名称","用例", "描述", "成功记录", "失败记录"]
        table_html = convert_list_to_table(head_list, category_data)
        html.extend(table_html)
        html.append("<script>")
        html.append("var space = document.getElementsByTagName(\"th\").length - 1;")
        html.append("var td_list = document.getElementsByTagName(\"td\");")
        html.append("for(var i=space; i< td_list.length; i=i+space+1){")
        html.append("var c = td_list[i-space].innerText;")
        html.append("if (td_list[i].innerText==0){ continue }")
        html.append("td_list[i].innerHTML='<a href=\"' + c + '.html\">' + td_list[i].innerText +  '</a>'; ")
        html.append("}")
        html.append("</script>")
        html.append("</html>")
        report_path = os.path.join(report_root, categroy, "{}.html".format(categroy))
        content = "".join(html)
        with open(report_path, 'w', encoding="utf-8") as f:
            f.write(content)

    @classmethod
    def print_check(clz):
        clz.collect_exception()
        html = []
        html.append("<html><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"/><body>")
        html.append("<h3>")
        html.append("配置表自检")
        html.append("</h3>")
        head_list = ["表名", "sheet名", "tag", "key", "信息"]
        table_html = convert_list_to_table(head_list, clz.exceptions)
        html.extend(table_html)
        html.append("</html>")
        report_root = clz.get_config("report_root")
        report_path = os.path.join(report_root, "check.html")
        content = " ".join(html)
        with open(report_path, 'w', encoding="utf-8") as f:
            f.write(content)

    @classmethod
    def set_config(clz, key, value):
        clz._config[key] = value

    @classmethod
    def get_config(clz, key):
        return clz._config.get(key)
    
    @classmethod
    def collect_exception(clz):
        for table_name in clz.pool:
            exception_info = clz.pool.get(table_name).get_exception_info()
            if len(exception_info) > 0:
                clz.exceptions.extend(exception_info)
    
    @classmethod
    def merge_translate(clz):
        clz._loader.load_match("Language")
        for table_name in clz.pool:
            if table_name.find("Language") >=0 and table_name != "Language":
                clz.pool["Language"].chain(clz.pool.get(table_name))

    @classmethod
    def merge_reward(clz):
        clz._loader.load_match("RewardConfig")
        for table_name in clz.pool:
            if table_name.find("RewardConfig") >=0 and table_name != "RewardConfig":
                clz.pool["RewardConfig"].chain(clz.pool.get(table_name))

    @classmethod
    def test(clz):
        print("call test", clz)

    @classmethod
    def test_one(clz, category, clss):
        report_root = clz.get_config("report_root")
        module = None
        print("Cases.{}.{}".format(category, clss))
        try:
            module = importlib.import_module("Cases.{}.{}".format(category, clss))
        except Exception as e:
            print(e)
        instance = module.__dict__[clss](clss, category)
        instance.run()
        instance.dump_detail_report(report_root)
        clz.need_recheck = instance.get_fail_case()


