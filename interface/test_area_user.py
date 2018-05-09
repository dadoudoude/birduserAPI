# coding:utf-8
import requests
import json
import urllib3
import unittest
import re
import time
import HTMLTestRunner

urllib3.disable_warnings()

class Test(unittest.TestCase):

    def setUp(self):
        print("start")
    def tearDown(self):
        print("end")

    #围栏用户
    def test02(self):
        #登录页
        host='http://bird.test.druidtech.net'
        #内容页
        hosts='https://bird.test.druidtech.net'
        #首页get请求
        r=requests.get(host)
        #打印状态码10*、20*、30*、40*、50*
        print("status",r.status_code)
        #打印get到的网页内容
        print(r.text)

        #login 登录请求
        namepassword={"username":"ceshiwushan","password":"337f18719259e77cc7519a21fd4c230b21917b18d5c6cfd68501c9275339c6ea"}
        #把登录请求数据转为json格式
        npdata=json.dumps(namepassword)
        #传入json格式的登录数据，post登录，    verify=False忽略SSL整数的验证，使访问https不报错
        login=requests.post('https://bird.test.druidtech.net'+'/api/v2/login',npdata,verify=False)
        #打印登录状态码
        print("status",login.status_code)
        #打印登录后返回的内容
        print("login.text",login.text)
        #打印header中的X-Druid-Authentication内容（该web以此作为身份认证）
        print("loginheader",login.headers['X-Druid-Authentication'])

        #header  请求每个url都需要的
        header={
        "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)"}


        #create area
        area={"distance":531,"point":{"lat":38.0466246,"lng":114.50832},"type":"Round","area_name":"石家庄API","msg_type":2}
        areadata=json.dumps(area)
        createarea=requests.post(hosts+'/api/v2/ditu/area',areadata,headers=header,verify=False)
        self.assertEquals(201,createarea.status_code)

        #get areas
        getareas1=requests.get(hosts+'/api/v2/ditu/area',headers=header,verify=False)
        self.assertEquals(200,getareas1.status_code)
        self.assertIn("石家庄API",getareas1.text)
        #获取areaid
        data1=eval(getareas1.text)
        areaid=data1[0]['id']
        #areas1 = re.findall(r'"id":"([^","]+)?', getareas1.text)  #正则表达式获取areaid  能用eval语法就用，其次是分片取值（备注：eval不支持元素为NULL）
        #str1=str(areas1)
        #areaid=str1[2:26]
        print("areaid",areaid)

        #修改围栏信息
        areainfo={"type":"Round","area_name":"修改后名称","msg_type":2,"distance":531,"point":{"lng":114.50832,"lat":38.0466246}}
        areainfodata=json.dumps(areainfo)
        putarea=requests.put(hosts+'/api/v2/ditu/area/'+areaid,areainfodata,headers=header,verify=False)
        self.assertEquals(201,putarea.status_code)
        #get areas
        getareas2=requests.get(hosts+'/api/v2/ditu/area',headers=header,verify=False)
        self.assertIn("修改后名称",getareas2.text)

        #get deviceid
        getdevicebymark=requests.get(hosts+'/api/v2/device/search/2088',headers=header,verify=False)
        #正则表达式获取Deviceid
        data2=eval(getdevicebymark.text)
        deviceid=data2[0]['id']
        #devices1 = re.findall(r'"id":"([^","]+)?', getdevicebymark.text)
        #str1=str(devices1)
        #deviceid=str1[2:26]
        print("deviceid",deviceid)

        #put device to area
        device={"id":[deviceid]}
        devicedata=json.dumps(device)
        putdevicetoarea=requests.put(hosts+'/api/v2/ditu/area/'+areaid+'/adddevice',devicedata,headers=header,verify=False)
        self.assertEquals(201,putdevicetoarea.status_code)

        #get area of devices
        getareaofdevices=requests.get(hosts+'/api/v2/device/',headers=header,verify=False)
        print(getareaofdevices.status_code)
        print(getareaofdevices.text)

        #get area by device id
        getareabydeviceid=requests.get(hosts+'/api/v2/device/id/'+deviceid+'/area',headers=header,verify=False)
        self.assertEquals(200,getareabydeviceid.status_code)
        self.assertIn("修改后名称",getareabydeviceid.text)

        #delete device from area
        deletedevicefromarea=requests.put(hosts+'/api/v2/ditu/area/'+areaid+'/deldevice',devicedata,headers=header,verify=False)
        self.assertEquals(201,deletedevicefromarea.status_code)

        #delete area
        deletearea=requests.delete(hosts+'/api/v2/ditu/area/'+areaid,headers=header,verify=False)
        self.assertEquals(204,deletearea.status_code)

        #create user
        userinfo={"username":"ceshi007","role":"user","email":"13512345678@163.com","phone":"13512345678","address":"四川省成都市高新区99号","password":"65c3f26f47c755357e081e775c5cee9eead2d69f0c07769a3f6daa733273dcfb"}
        userdata=json.dumps(userinfo)
        createuser=requests.post(hosts+'/api/v2/user/',userdata,headers=header,verify=False)
        self.assertEquals(201,createuser.status_code)

        #get user
        getuser=requests.get(hosts+'/api/v2/user/',headers=header,verify=False)
        self.assertEquals(200,getuser.status_code)
        self.assertIn("ceshi007",getuser.text)
        #正则表达式获取userid
        #da1=eval(getuser.text)   #由于eval不支持json出现null情况，所以暂时使用正则
        #userid=da1[0]['id']
        users1 = re.findall(r'"id":"([^","]+)?', getuser.text)
        str3=str(users1)
        userid=str3[2:26]
        print("userid",userid)

        #Get Myself Info
        getmyselfinfo=requests.get(hosts+'/api/v2/user/me',headers=header,verify=False)
        self.assertEquals(200,getmyselfinfo.status_code)
        self.assertIn("username",getmyselfinfo.text)

        #authority授权
        auth={"sim_auth":0,"search_auth":0,"company_auth":0,"device_auth":0,"data_auth":0,"platform_auth":0,"firmware_auth":0,"setting_auth":3,"user_auth":3,"export_auth":1,"biological_auth":3,"env_auth":1,"bhv_auth":1,"analysis_auth":1}
        authdata=json.dumps(auth)
        setauth=requests.post(hosts+'/api/v2/user/id/'+userid+'/edit_auth',authdata,headers=header,verify=False)
        self.assertEquals(201,setauth.status_code)

        #add device to user
        add={"id":[deviceid]}
        adddata=json.dumps(add)
        adddevice=requests.post(hosts+'/api/v2/user/id/'+userid+'/add_auth',adddata,headers=header,verify=False)
        self.assertEquals(201,adddevice.status_code)

        #List Devices Info
        listdevicesinfo=requests.get(hosts+'/api/v2/user/id/'+userid+'/device',headers=header,verify=False)
        self.assertEquals(200,listdevicesinfo.status_code)
        self.assertIn("updated_at",listdevicesinfo.text)

        #GET User With id
        getuserwithid=requests.get(hosts+'/api/v2/user/id/'+userid,headers=header,verify=False)
        self.assertEquals(200,getuserwithid.status_code)
        self.assertIn("username",getuserwithid.text)

        #delete device from user
        deletedevice=requests.post(hosts+'/api/v2/user/id/'+userid+'/del_auth',adddata,headers=header,verify=False)
        self.assertEquals(204,deletedevice.status_code)

        #change user password
        password={"old_password":"337f18719259e77cc7519a21fd4c230b21917b18d5c6cfd68501c9275339c6ea","password":"cecfc3602f3a59347e44d7b684f739d8d6004f2b9a86c3202b357988c27d4283"}
        passworddata=json.dumps(password)
        changeuserpassword=requests.put(hosts+'/api/v2/user/id/'+userid+'/password',passworddata,headers=header,verify=False)
        self.assertEquals(201,changeuserpassword.status_code)

        #delete user
        deleteuser=requests.delete(hosts+'/api/v2/user/id/'+userid,headers=header,verify=False)
        self.assertEquals(204,deleteuser.status_code)

        #Get Company
        getcompany=requests.get(hosts+'/api/v2/company/',headers=header,verify=False)
        print("company",getcompany.text)

        #List Firmware
        listfirmware=requests.get(hosts+'/api/v2/firmware/',headers=header,verify=False)
        print("firmware",listfirmware.text)
        firm=eval(listfirmware.text)
        firmid=firm[0]['id']
        print("firmid",firmid)

        #Download Firmware with ID
        dlfirm=requests.get(hosts+'/api/v2/firmware/download/'+firmid,headers=header,verify=False)
        self.assertEquals(200,dlfirm.status_code)
