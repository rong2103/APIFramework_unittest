'''
__author__ = ‘zhourong‘
'''
# -*- coding: utf-8 -*-
import requests
import json

class MyRequests:
    def __init__(self,logger):
        self.logger = logger

    def myrequest(self,url,method,request_data,headers):
        # 判断如果请求数据不为空就将请求数据转换成字典类型，如果请求数据为空就直接传数据None
        if request_data is not None:
            request_data = eval(request_data)
            # request_data = json.dumps(request_data)
            headers = eval(headers)
            self.logger.info("转换为字典后的请求数据为{0}".format(request_data))
            self.logger.info("转换为字典后的请求数据类型为{0}".format(type(request_data)))
            self.logger.info("转换为字典后的请求头为{0}".format(headers))
            self.logger.info("转换为字典后的请求头类型为{0}".format(type(headers)))
        if method == "get":
            if (headers is not None) and ("Content-Type" in headers.keys()):
                # if "Content-Type" in headers.keys():
                if headers["Content-Type"] == "application/json":
                    res = requests.get(url, json.dumps(request_data), headers=headers)
            else:
                res = requests.get(url, request_data, headers=headers)
        elif method == "post":
            if (headers is not None) and ("Content-Type" in headers.keys()):
                # if "Content-Type" in headers.keys():
                if headers["Content-Type"] == "application/json":
                    res = requests.post(url, json.dumps(request_data), headers=headers)
            else:
                res = requests.post(url, request_data, headers=headers)
        elif method == "put":
            if (headers is not None) and ("Content-Type" in headers.keys()):
                # if "Content-Type" in headers.keys():
                if headers["Content-Type"] == "application/json":
                    res = requests.put(url, json.dumps(request_data), headers=headers)
            else:
                res = requests.put(url, request_data, headers=headers)
            # if headers == None:
            #     res = requests.put(url, request_data)
            # else:
            #     res = requests.put(url, request_data, headers=headers)
        elif method == "delete":
            if (headers is not None) and ("Content-Type" in headers.keys()):
                # if "Content-Type" in headers.keys():
                if headers["Content-Type"] == "application/json":
                    res = requests.delete(url, json.dumps(request_data), headers=headers)
            else:
                res = requests.delete(url, data=request_data,headers=headers)
        else:
            self.logger.info("请求方法没有找到")
            res = None
        return res
