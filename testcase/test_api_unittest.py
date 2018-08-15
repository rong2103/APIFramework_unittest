import unittest
from common import dirconfig
from common.log import Log
from common.myexcel import MyExcel
from common.myrequests import MyRequests
import ddt
import time
import re

#new logger
now = time.strftime('%Y-%m-%d_%H_%M_%S')
logger = Log("zhourong", dirconfig.logger_dir + "/log" + now + ".txt")
# logger = Log("zhourong", dirconfig.logger_dir + "/log"  + ".txt")
#init_variables:全局变量字典
filename = dirconfig.testcase_dir + "/api.xlsx"
sheetname2 = "variables"
fileobj = MyExcel(filename,logger)
init_variables = fileobj.get_init_variables(sheetname2)

#获取excel中所有用例数据存在testdatas中，为ddt参数做准备
sheetname1 = "PMS"
# sheetname1 = u"已完成"
testdatas = fileobj.getallrow(sheetname1)
request = MyRequests(logger)
dynamic_varis_dict = {}

@ddt.ddt
class TestAPI(unittest.TestCase):
    #tearDown与tearDownClass的区别：
    # 前者每个用例前后都要执行（有多少个测试用例就执行多少次）；
    # 后者在测试类中所有用例执行前后执行一次（只执行一次）

    # @classmethod
    # def tearDownClass(cls):
    #     #更新注册的电话号码变量
    #     fileobj.update_init_data(sheetname2,2,2)
    #     fileobj.savefile(filename)

    #@ddt.data(*testdatas)中参数不能用self.testdatas的形式，所以将testdatas的数据放在类外面
    #有ddt之后就不用for循环了
    @ddt.data(*testdatas)
    def test_api(self,testdata):
        global dynamic_varis_dict
        logger.info("=====================接口测试开始=====================")
        logger.info("现在执行的测试用例名为：{0}".format(testdata["case_name"]))
        logger.info("现在执行的测试用例数据为：{0}".format(testdata))
        logger.info("请求url为：{0}".format(testdata["ip"]+":"+testdata["port"]+testdata["absurl"]))
        logger.info("请求http_method为：{0}".format(testdata["http_method"]))
        logger.info("请求request_data为：{0}".format(testdata["request_data"]))
        logger.info("请求request_data类型为：{0}".format(type(testdata["request_data"])))
        logger.info("请求related_expression为：{0}".format(testdata["related_expression"]))
        logger.info("请求related_expression类型为：{0}".format(type(testdata["related_expression"])))
        ################################
        # # if testdata["request_data"].find()
        #判断请求是否需要替换
        logger.info("dynamic_varis_dict:{0}".format(dynamic_varis_dict))
        dynamic_varis_len = len(dynamic_varis_dict)
        logger.info("动态变量的长度为：{0}".format(dynamic_varis_len))
        if len(dynamic_varis_dict) == 0:
            pass
        else:
            for key,value in dynamic_varis_dict.items():
                logger.info("动态变量的key为：{0}".format(key))
                if testdata["absurl"].find(key) != -1:
                    logger.info("请求中包含key")
                    testdata["absurl"] = testdata["absurl"].replace(key, str(value))
                if testdata["request_data"].find(key)!= -1:
                     logger.info("请求中包含key")
                     testdata["request_data"] = testdata["request_data"].replace(key, str(value))
                # if testdata["related_expression"].find(key)!= -1:
                #      logger.info("related_expression中包含key")
                #      testdata["related_expression"] = testdata["related_expression"].replace(key, str(value))
                if testdata["request_header"].find(key)!=-1:
                    logger.info("请求头中包含key")
                    testdata["request_header"] = testdata["request_header"].replace(key, str(value))
        url1=testdata["ip"]+":"+testdata["port"]+testdata["absurl"]
        #打印变量替换后的各个请求数据
        logger.info("变量替换后的请求url为：{0}".format(testdata["absurl"]))
        logger.info("变量替换后的请求request_data为：{0}".format(testdata["request_data"]))
        logger.info("变量替换后的请求request_header为：{0}".format(testdata["request_header"]))
        #执行请求
        res = request.myrequest(url1, testdata["http_method"],testdata["request_data"],testdata["request_header"])
        logger.info("返回的响应数据为：{0}".format(res.text))
        logger.info("返回的响应类型为：{0}".format(type(res.text)))
        logger.info("期望结果为为：{0}".format(testdata["expected_data"]))
        # 判断该用例是否要做响应数据提取
        if testdata["related_expression"] =="None":
            logger.info("不需要做响应提取")
        else:
            # testdata["related_expression"] is not None:
            logger.info("需要做响应提取")
            #${loanid}=.*"id":(\d*)[^\S]?"memberId":"${userid}"
            temp = testdata["related_expression"].split("=")
            logger.info("提取变量名为：{0}".format(temp[0]))
            logger.info("正则表达式的值为：{0}".format(temp[1]))
            #需要添加判断，如果变量名存在，变量名不变，只更新值；如果变量名不存在，则加一条key
            #正则匹配变量值
            #匹配时判断时匹配最后一个值还是匹配第一个值
            if testdata["match_location"] == "None":
                res_id = re.findall(temp[1],res.text)[0]
            else:
                res_id_list = re.findall(temp[1], res.text)
                res_id_len=len(res_id_list)
                res_id=res_id_list[res_id_len-1]
            logger.info("res_id:".format(res_id))
            #{"$user_id":"2211"}
            #将匹配的变量值给变量名
            dynamic_varis_dict[temp[0]] = res_id
            logger.info("动态变量为：{0}".format(dynamic_varis_dict))
        #断言方式判断
        if int(testdata["compare_type"]) == 0:
            logger.info("全值匹配断言")
            assert res.text == testdata["expected_data"]
        elif int(testdata["compare_type"]) == 1:
            logger.info("部分匹配断言")
            # 可用正则表达式，更灵活
            self.assertIn(testdata["expected_data"],res.text)
        logger.info("=====================接口测试结束=====================")

