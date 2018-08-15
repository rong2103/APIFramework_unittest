'''
__author__ = ‘zhourong‘
'''
# -*- coding: utf-8 -*-
import requests
import json
url="http://192.168.10.203:5556/r-jte/pms-biz/home-page/repair-room"
data=[{"roomCode":"203956737500778496","roomNumber":"1003","roomTypeCode":"03956492578590720","hotelCode":"0736466262620180612044309","groupCode":"0736466262620180612044309","beginDate":"2018-10-09 10:47:46","endDate":"2018-10-09 10:54:49","operator":"a","isDirty":"0"},{"roomCode":"203956737739853824","roomNumber":"1008","roomTypeCode":"03956492578590720","hotelCode":"0736466262620180612044309","groupCode":"0736466262620180612044309","beginDate":"2018-08-09 10:47:46","endDate":"2018-08-09 10:54:49","operator":"a","isDirty":"0"}]
headers={"ticket":"0fcc9d61-8652-4f1f-bfe2-d01e3072a979","Content-Type":"application/json"}
# for i in (0,len(data)-1):
#     print(data[i])
#     print(type(data[i]))
res = requests.post(url, json.dumps(data), headers=headers)
print(res.text)
# headers={"ticket":"${ticket}","Content-Type":"application/json"}


