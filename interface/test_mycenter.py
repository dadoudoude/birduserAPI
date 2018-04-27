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

    #个人中心
    def test03(self):
        host='http://bird.test.druidtech.net'
        hosts='https://bird.test.druidtech.net'
        r=requests.get(host)
        print("status",r.status_code)
        #print(r.text)

        #login
        namepassword={"username":"ceshiwushan","password":"337f18719259e77cc7519a21fd4c230b21917b18d5c6cfd68501c9275339c6ea"}
        npdata=json.dumps(namepassword)
        login=requests.post('https://bird.test.druidtech.net'+'/api/v2/login',npdata,verify=False)
        print("status",login.status_code)
        print("login.text",login.text)
        print("loginheader",login.headers['X-Druid-Authentication'])

        #header
        header={
        "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)"}

        #get myself
        getmyself=requests.get(hosts+'/api/v2/user/myself',headers=header,verify=False)
        self.assertEquals(200,getmyself.status_code)
        self.assertIn("username",getmyself.text)

        #get deviceid
        getdevicebymark=requests.get(hosts+'/api/v2/device/search/2088',headers=header,verify=False)
        #get deviceid
        data11=eval(getdevicebymark.text)
        deviceid=data11[0]['id']

        #update myinfo
        myinfo={"phone":"135123456789666","email":"1236666@163.com","address":"1231266666"}
        infodata=json.dumps(myinfo)
        updatemyinfo=requests.put(hosts+'/api/v2/user/info',infodata,headers=header,verify=False)
        self.assertEquals(201,updatemyinfo.status_code)

        # 导出数据csv多个设备
        device={"id":[deviceid]}
        devicedata=json.dumps(device)
        exportdata1=requests.post(hosts+'/api/v2/device/csv_multiple',devicedata,headers=header,verify=False)
        self.assertEquals(200,exportdata1.status_code)


        #get unread message
        getunreadmessage=requests.get(hosts+'/api/v2/message/unread',headers=header,verify=False)
        self.assertEquals(200,getunreadmessage.status_code)
        print(getunreadmessage.text)
        #get messageid
        data12=eval(getunreadmessage.text)
        messageid=data12[0]['id']

        #PUT message read 标记已读
        message={"id":[messageid]}
        messagedata=json.dumps(message)
        putmessageread=requests.put(hosts+'/api/v2/message/',messagedata,headers=header,verify=False)
        self.assertEquals(201,putmessageread.status_code)

        #delete message by id
        deletemessage=requests.delete(hosts+'/api/v2/message/id/'+messageid,headers=header,verify=False)
        self.assertEquals(204,deletemessage.status_code)

        #导出数据产生通知消息
        exportdata2=requests.post(hosts+'/api/v2/device/kml_multiple',devicedata,headers=header,verify=False)
        self.assertEquals(200,exportdata2.status_code)
        #获取messageid
        getunreadmessage2=requests.get(hosts+'/api/v2/message/unread',headers=header,verify=False)
        self.assertEquals(200,getunreadmessage2.status_code)
        print(getunreadmessage2.text)
        #get messageid
        data13=eval(getunreadmessage2.text)
        print("test ",data13[0]['id'])
        messageid2=data13[0]['id']
        #删除所有message
        message2={"id":[messageid2]}
        messagedata2=json.dumps(message2)
        deletemessages=requests.put(hosts+'/api/v2/message/delete',messagedata2,headers=header,verify=False)
        self.assertEquals(204,deletemessages.status_code)

        #导出数据 csv单个设备
        exportdata3=requests.post(hosts+'/api/v2/device/csv',devicedata,headers=header,verify=False)
        self.assertEquals(200,exportdata3.status_code)

        #导出excel单个文件
        exportdata4=requests.post(hosts+'/api/v2/device/excel',devicedata,headers=header,verify=False)
        self.assertEquals(200,exportdata4.status_code)

        #导出excel多个文件
        exportdata5=requests.post(hosts+'/api/v2/device/excel_multiple',devicedata,headers=header,verify=False)
        self.assertEquals(200,exportdata5.status_code)

        #GET Many Device
        exportdata6=requests.post(hosts+'/api/v2/device/many',devicedata,headers=header,verify=False)
        self.assertEquals(200,exportdata6.status_code)

        #Exclude Device
        exportdata7=requests.post(hosts+'/api/v2/device/exclude',devicedata,headers=header,verify=False)
        self.assertEquals(200,exportdata7.status_code)

        #获取messageid
        unreadme=requests.get(hosts+'/api/v2/message/unread',headers=header,verify=False)
        #get messageid
        da1=eval(unreadme.text)
        print("test ",da1[0]['id'])
        mes1=da1[0]['id']
        mes2=da1[1]['id']
        mes3=da1[2]['id']

        message3={"id":[mes1,mes2,mes3]}
        messagedata3=json.dumps(message3)
        deleteallme=requests.put(hosts+'/api/v2/message/delete',messagedata3,headers=header,verify=False)
        self.assertEquals(204,deleteallme.status_code)






        #个人设置
        #设置【设备】的｛运营商、备注｝隐藏
        deviceset1={"fields":["firmware_version","device_type"]}
        setdata1=json.dumps(deviceset1)
        putdevice=requests.put(hosts+'/api/v2/user/fields/device',setdata1,headers=header,verify=False)
        self.assertEquals(201,putdevice.status_code)
        #设置【环境数据】的｛光照、网络强度、气压、湿度｝隐藏
        envset={"fields":["activity_expend","description","firmware_version","altitude","dimension","course","speed","used_star","temperature"]}
        setdata2=json.dumps(envset)
        putenv=requests.put(hosts+'/api/v2/user/fields/env',setdata2,headers=header,verify=False)
        self.assertEquals(201,putenv.status_code)
        #设置【行为数据】的｛活动强度｝隐藏
        behset={"fields":["mark","description","firmware_version"]}
        setdata3=json.dumps(behset)
        putbeh=requests.put(hosts+'/api/v2/user/fields/behavior',setdata3,headers=header,verify=False)
        self.assertEquals(201,putbeh.status_code)
        #设置【短信数据】的｛湿度、光照、气压、网络强度、固件｝隐藏
        smsset={"fields":["mark","device_type","network_operator","altitude","dimension","course","speed","used_star","temperature"]}
        setdata4=json.dumps(smsset)
        putsms=requests.put(hosts+'/api/v2/user/fields/sms',setdata4,headers=header,verify=False)
        self.assertEquals(201,putsms.status_code)
        #设置时区UTC+0 分页20
        setprofile={"page_size":20,"time_zone":0}
        prodata=json.dumps(setprofile)
        putpro=requests.put(hosts+'/api/v2/user/profile',prodata,headers=header,verify=False)
        self.assertEquals(201,putpro.status_code)
        #getmyself验证设置是否成功
        getmyself2=requests.get(hosts+'/api/v2/user/myself',headers=header,verify=False)
        self.assertEquals(200,getmyself2.status_code)
        self.assertIn('"device_fields":{"fields":["firmware_version","device_type"]},"env_fields":{"fields":["activity_expend","description","firmware_version","altitude","dimension","course","speed","used_star","temperature"]},"behavior_fields":{"fields":["mark","description","firmware_version"]},"sms_fields":{"fields":["mark","device_type","network_operator","altitude","dimension","course","speed","used_star","temperature"]}',getmyself2.text)
        self.assertIn('"page_size":20,"time_zone":0,"',getmyself2.text)
