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

    #设备
    def test01(self):
        host='http://bird.test.druidtech.net'
        hosts='https://bird.test.druidtech.net'
        #mark='2088'

        r=requests.get(host)
        #print("status",r.status_code)

        #login
        namepassword={"username":"ceshiwushan","password":"337f18719259e77cc7519a21fd4c230b21917b18d5c6cfd68501c9275339c6ea"}
        npdata=json.dumps(namepassword)
        login=requests.post('https://bird.test.druidtech.net'+'/api/v2/login',npdata,verify=False)
        #print("status",login.status_code)
        #print("login.text",login.text)
        #print("loginheader",login.headers['X-Druid-Authentication'])

        #header
        header={
        "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)"}


        #
        #List Devices
        listdevices=requests.get(hosts+'/api/v2/device/',headers=header,verify=False)
        mark1=eval(listdevices.text)[-1]['mark']
        mark=str(mark1)
        print("mark",mark)

        #Search Device By mark
        getdevicebymark=requests.get(hosts+'/api/v2/device/search/'+mark,headers=header,verify=False)
        #print(getdevicebymark.text)
        #正则表达式获取Deviceid
        devices1 = re.findall(r'"id":"([^","]+)?', getdevicebymark.text)
        str1=str(devices1)
        deviceid=str1[2:26]
        print("deviceid",deviceid)

        #get device by id
        getdevicebyid=requests.get(hosts+'/api/v2/device/id/'+deviceid,headers=header,verify=False)
        self.assertIn("updated_at",getdevicebyid.text)
        #print("getdevicebyid.text",getdevicebyid.text)

        #get device setting by deviceid
        getsetting=requests.get(hosts+'/api/v2/setting/device/'+deviceid,headers=header,verify=False)
        print(getsetting.status_code,getsetting.text)
        self.assertIn("uuid",getsetting.text)
        self.assertEquals(200,getsetting.status_code)
        print("getsetting.text",getsetting.text)

        #get settings
        getsettings=requests.get(hosts+'/api/v2/setting/',headers=header,verify=False)
        self.assertEquals(200,getsettings.status_code)
        self.assertIn("gprs_retries",getsettings.text)

        #put device setting
        devicesetting={"env_sampling_mode":1,"env_sampling_freq":600,"env_voltage_threshold":3.7,"behavior_sampling_mode":1,"behavior_sampling_freq":600,"behavior_voltage_threshold":3.8,"gprs_mode":1,"gprs_freq":86400,"gprs_voltage_threshold":3.8}
        settingdata=json.dumps(devicesetting)
        putdevicesetting=requests.put(hosts+'/api/v2/setting/device/'+deviceid,settingdata,headers=header,verify=False)
        self.assertEquals(201,putdevicesetting.status_code)

        #get biological by deviceid
        getbiological=requests.get(hosts+'/api/v2/biological/device/'+deviceid,headers=header,verify=False)
        self.assertEquals(200,getbiological.status_code)
        self.assertIn("species",getbiological.text)
        #print("getbiological.text",getbiological.text)

        #put device biological by deviceid
        biological={"age":1,"bid":"API测试鸟","blood":"1","note":"这是API测试的生物信息。","gender":1,"latitude":"50","location":"四川省成都市","longitude":"110","species":"公鸡","head_length":233,"timestamp":"2018-04-11T07:02:36.150Z","weight":5000,"wing_length":999,"label":"[neck,beak,back,leg]","feather":"[head,breast,covert,tail]","swab":"[anal,throat]","culmen_length":666,"tarsus_length":444,"tail_length":666,"wingspan":555,"body_length":999}
        biologicaldata=json.dumps(biological)
        putbiological=requests.post(hosts+'/api/v2/biological/bird/'+deviceid,biologicaldata,headers=header,verify=False)
        self.assertEquals(201,putbiological.status_code)

        #get gps by deviceid
        getgps=requests.get(hosts+'/api/v2/gps/device/'+deviceid,headers=header,verify=False)
        self.assertEquals(200,getgps.status_code)
        self.assertIn("point_location",getgps.text)
        #print("getgps.text",getgps.text)

        #List GPS
        getallGPS=requests.get(hosts+'/api/v2/gps/',headers=header,verify=False)
        self.assertEquals(200,getallGPS.status_code)
        self.assertIn("timestamp",getallGPS.text)

        #get gps 图表
        getgpspicture=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'?last=-3',headers=header,verify=False)
        self.assertEquals(200,getgpspicture.status_code)
        self.assertIn("point_location",getgpspicture.text)
        print(getgpspicture.text)
        #设置时间查询
        getgpswithtime=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'?last=-3&begin=2018-02-05T06:31:59.619Z&end=2018-04-11T06:31:59.619Z',headers=header,verify=False)
        self.assertEquals(200,getgpswithtime.status_code)

        #get gps 默认轨迹(最近3个月)
        getgps3=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/line?last=-3',headers=header,verify=False)
        self.assertEquals(200,getgps3.status_code)
        #get gps 最近6个月
        getgps6=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/line?last=-6',headers=header,verify=False)
        self.assertEquals(200,getgps6.status_code)
        #get gps 最近12个月
        getgps12=requests.get(hosts+'/api/v2/gps/device/'+deviceid+'/line?last=-12',headers=header,verify=False)
        self.assertEquals(200,getgps12.status_code)

        #圆形范围搜索设备
        ditucir={"max":85,"point":[104.0609176,30.5483632]}
        ditucirdata=json.dumps(ditucir)
        searchcir=requests.post(hosts+'/api/v2/ditu/',ditucirdata,headers=header,verify=False)
        self.assertEquals(200,searchcir.status_code)
        self.assertIn("device_id",searchcir.text)

        #多边形范围搜索设备
        ditupol={"polygon":[[[104.0601841,30.5486184],[104.0604572,30.5479021],[104.0618706,30.5476413],[104.0621276,30.5485323],[104.0612977,30.5488337],[104.0601841,30.5486184]]]}
        ditupoldata=json.dumps(ditupol)
        searchpol=requests.post(hosts+'/api/v2/ditu/',ditupoldata,headers=header,verify=False)
        self.assertEquals(200,searchpol.status_code)
        self.assertIn("device_id",searchpol.text)

        #Get GPS Section
        #sec={"devices":deviceid}
        #secdata=json.dumps(sec)
        #getGPSsec=requests.put(hosts+'/api/v2/gps/section',secdata,headers=header,verify=False)
        #print("1",getGPSsec.status_code)
        #print("2",getGPSsec.text)

        #Get Behavior By DeviceID
        getbehavior=requests.get(hosts+'/api/v2/behavior/device/'+deviceid,headers=header,verify=False)
        self.assertEquals(200,getbehavior.status_code)
        self.assertIn("company_id",getbehavior.text)

        #List Behavior
        getbehaviors=requests.get(hosts+'/api/v2/behavior/',headers=header,verify=False)
        self.assertEquals(200,getbehaviors.status_code)
        self.assertIn("company_id",getbehaviors.text)

        #Get bird by device id
        getbird=requests.get(hosts+'/api/v2/biological/device/'+deviceid,headers=header,verify=False)
        self.assertEquals(200,getbird.status_code)
        self.assertIn("updated_at",getbird.text)

        #环境数据翻页
        gpsheaderp3={
            "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-sort":"-timestamp",
            "x-result-limit":"100",
            "x-result-offset":"200"
        }
        gpsp3=requests.get(hosts+'/api/v2/gps/device/'+deviceid,headers=gpsheaderp3,verify=False)
        self.assertEquals(200,gpsp3.status_code)
        self.assertIn("company_id",gpsp3.text)

        gpsheaderp2={
            "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-sort":"-timestamp",
            "x-result-limit":"100",
            "x-result-offset":"200"
        }
        gpsp2=requests.get(hosts+'/api/v2/gps/device/'+deviceid,headers=gpsheaderp2,verify=False)
        self.assertEquals(200,gpsp2.status_code)
        self.assertIn("company_id",gpsp2.text)

        #行为数据翻页
        bhheaderp3={
            "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-sort":"-timestamp",
            "x-result-limit":"20",
            "x-result-offset":"40"
        }
        bhp3=requests.get(hosts+'/api/v2/behavior/device/'+deviceid,headers=bhheaderp3,verify=False)
        self.assertEquals(200,bhp3.status_code)
        self.assertIn("company_id",bhp3.text)

        bhheaderp2={
            "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-sort":"-timestamp",
            "x-result-limit":"20",
            "x-result-offset":"20"
        }
        bhp2=requests.get(hosts+'/api/v2/behavior/device/'+deviceid,headers=bhheaderp2,verify=False)
        self.assertEquals(200,bhp2.status_code)
        self.assertIn("company_id",bhp2.text)

        #短信数据翻页
        smsheaderp3={
            "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-sort":"-timestamp",
            "x-result-limit":"10",
            "x-result-offset":"10"
        }
        smsp3=requests.get(hosts+'/api/v2/gps/device/5881e103f01fce1212f038a4/sms',headers=smsheaderp3,verify=False)
        self.assertEquals(200,smsp3.status_code)
        self.assertIn("company_id",smsp3.text)

        smsheaderp2={
            "Connection": "keep-alive",
            "conten-type": "application/json; text/plain; charset=utf-8; multipart/form-data",
            "content-disposition": "form-data; name='imgType'",
            "Accept-Encoding": "gzip, deflate, br",
            "x-druid-authentication":login.headers['X-Druid-Authentication'],
            "Host": "bird.test.druidtech.net",
            "User-Agent": "Apache-HttpClient/4.5.5 (Java/1.8.0_144)",
            "x-result-sort":"-timestamp",
            "x-result-limit":"10"
        }
        smsp2=requests.get(hosts+'/api/v2/gps/device/5881e103f01fce1212f038a4/sms',headers=smsheaderp2,verify=False)
        self.assertEquals(200,smsp2.status_code)
        self.assertIn("company_id",smsp2.text)





