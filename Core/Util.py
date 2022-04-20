#coding=utf-8
"""
这里是一些常用的工具方法
"""

from operator import index
from pandas import array


def convert_list_to_table(head_list, body_list):
    if len(head_list) <= 0 or len(body_list) <0:
        return ""
    html = []
    html.append("<table border=\"3\"  bordercolor=\"violet\"><tr>")
    for h in head_list:
        html.append("<th>")
        html.append(h)
        html.append("</th>")
    html.append("</tr>")
    for body in body_list:
        html.append("<tr>")
        for b in body:
            html.append("<td>")
            html.append(str(b))
            html.append("</td>")
        html.append("</tr>")
    html.append("</table>")
    return html

def is_html():
    pass

def get_MDA_value(arr,indx):
    """
    获取多维数组中的某个下标值
    """
    if arr:
        pass