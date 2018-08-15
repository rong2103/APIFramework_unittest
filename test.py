'''
__author__ = ‘zhourong‘
'''
# -*- coding: utf-8 -*-
d=[{'related_expression': '${ticket}=.*\\"ticket\\":\\"(\\w*.*)\\"', 'http_method': 'post', '二级目录': '登录', '一级目录': '登录', 'port': '9023', 'request_header': '{"ticket":"${ticket}"}', 'compare_type': '1', 'case_id': '0001', 'absurl': '/login', 'api_name': '登录', 'expected_data': '{"code":0,', 'match_location': 'None', 'request_data': '{"referer":"http://192.168.10.204/pms/","uuid":"","username":"zr","password":"123456","captcha":""}', 'ip': 'http://192.168.10.204', 'case_name': '登录'}]
# print(d.__dict__)
# print(d.dir())
class A:
    def AA(self):
        print("AA")

a = A()
print(a.__dir__())
print(a.__dict__)