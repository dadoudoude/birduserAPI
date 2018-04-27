# coding:utf-8
import HTMLTestRunner
import json
import re
import unittest

import requests
import urllib3

urllib3.disable_warnings()

class Test(unittest.TestCase):
    def setUp(self):
        print("start")
    def tearDown(self):
        print("end")

    #设备
    def test04(self):
        #host='http://bird.test.druidtech.net'
        #hosts='https://bird.test.druidtech.net'
        #header = {"User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)"}
        hostname='https://bird.test.druidtech.net'
        r = requests.get('http://bird.test.druidtech.net',verify=False)

        #定义登录参数数组
        logindata1 = {"password":"337f18719259e77cc7519a21fd4c230b21917b18d5c6cfd68501c9275339c6ea","username":"ceshiwushan"}
        #转为json格式
        uspw_data1 = json.dumps(logindata1)
        #post登录请求
        login1 = requests.post('https://bird.test.druidtech.net/api/v2/login',uspw_data1,verify=False)
        print("loginheader",login1.headers)
        print("responsedata",login1.headers)
        print("xd",login1.headers['X-Druid-Authentication'])

        #创建header
        header1 = {
            "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login1.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)"}

        password1={"password":"daafcceb72ec0cc8c8c6eade8e4249a144f3318916ccadf22026dc7f57e67aee","old_password":"337f18719259e77cc7519a21fd4c230b21917b18d5c6cfd68501c9275339c6ea"}
        passworddata1=json.dumps(password1)
        change1=requests.put('https://bird.test.druidtech.net/api/v2/user/password',passworddata1,headers=header1,verify=False)
        print("status",change1.status_code)
        print(change1.text)



        #定义登录参数数组
        logindata2 = {"password":"daafcceb72ec0cc8c8c6eade8e4249a144f3318916ccadf22026dc7f57e67aee","username":"ceshiwushan"}
        #转为json格式
        uspw_data2 = json.dumps(logindata2)
        #post登录请求
        login2 = requests.post('https://bird.test.druidtech.net/api/v2/login',uspw_data2,verify=False)
        print("loginheader",login2.headers)
        print("responsedata",login2.headers)

        #创建header
        header2 = {
            "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login2.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)"}

        password2={"password":"337f18719259e77cc7519a21fd4c230b21917b18d5c6cfd68501c9275339c6ea","old_password":"daafcceb72ec0cc8c8c6eade8e4249a144f3318916ccadf22026dc7f57e67aee"}
        passworddata2=json.dumps(password2)
        change2=requests.put('https://bird.test.druidtech.net/api/v2/user/password',passworddata2,headers=header2,verify=False)
        print("status",change2.status_code)
        print(change2.text)

        #post登录请求
        login3 = requests.post('https://bird.test.druidtech.net/api/v2/login',uspw_data1,verify=False)
        print("loginheader",login3.headers)
        print("responsedata",login3.headers)

        #创建header
        header = {
            "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login3.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)"}
        #getmyself
        getmyself = requests.get('https://bird.test.druidtech.net/api/v2/user/myself',headers=header,verify=False)
        print(getmyself.status_code)
        self.assertEquals(getmyself.status_code,200)
        print("myinfo",getmyself.text)
        self.assertIn("ceshiwushan",getmyself.text)