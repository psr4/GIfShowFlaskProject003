from urllib import parse
import requests
import sys
sys.path.append("..")
from Config import config
import hashlib
import time
import copy

class GifLogin:
    def __init__(self):

        self.headers = config().HEADERS
        #print(type(self.headers))
        self.sig_data_ini= config().SIG_DATA
        self.salt = config().SALT
        self.token_salt = config().TOKEN_SALT
        self.sig_data = config().SIG_DATA
        self.phone = config().PHONE_NUMBER


    # 对data和headers做排序
    def sig_and_headers(self):
        sig_str = ""
        url_headers = {}
        head = list(self.headers)
        sig_key = self.headers
        #print(sig_key)
        print("最后的sigdata")
        print(self.sig_data)

        sig_key.update(self.sig_data)
        for i in sorted(list(sig_key)):
            sig_str = sig_str + i + "=" + sig_key[i]
        self.sig_str = sig_str
        #print(self.sig_str)
        head.sort()
        for i in head:
            url_headers[i] = self.headers[i]
        self.url_tail = parse.urlencode(url_headers)

    def get_final_data(self, sigdata):

        self.sig_and_headers()
        str = self.sig_str + self.salt
        print(str)
        m = hashlib.md5(str.encode())
        sig = m.hexdigest()
        data = {'sig': sig
            }
        data.update(self.sig_data)
        #print(data)
        return data
    def get_sig_data_aucode(self,phone):
        data = {'mobileCountryCode': '+86',
                'mobile': phone,
                'type': '27',
                }
        self.sig_data.update(data)
    def get_sig_data_verify(self,code):
        self.sig_data = self.sig_data_ini
        data = {'secret': 'kot+b9DmI8dUebDh4utqdbDr+wWLZt+Y7X8BIxVbgCkDcGpqw1Af669dE7PPb35yenhq7p4EnXZLlMD1HnHMGZbLFyMZiwNjsD29hW+qhLgMMUv0cFu50auJVQEI+0ZS2LQruJagOKnjqTV6HPQGFANDb+Vfrslt6Czz2YS/kB4L4s2HRajAc/ZdsFmh8qglFwKGoWfEFYrqqDLSYr1OdzapV+VifQ2j8K4Q/MobT/E0nUOrbj/IYN5PmY4Xfl0qXhM9uwQ3i6VbUtv5u1kh9QIgNpwVqX0Z3ifUjyTXi66CnanyXjzWU/XXPVzN050HD1FZVUyRhXdA09anE5Mn5Q==',
                'raw': '1599101098761',
                'type': '27',
                'mobileCountryCode': '+86',
                'mobile': str(self.phone),
                'code': str(code),
                }
        self.sig_data.update(data)
        del self.sig_data["kuaishou.api_st"]
        del self.sig_data["token"]

    def get_sig_data_token(self,logintype,smscode,logintoken):
        #print(self.sig_data_ini)
        self.sig_data = self.sig_data_ini

        data = {'loginType': str(logintype),
                'smsCode': str(smscode),
                'loginToken': logintoken,
                'userId': '1942009504',
                'giveUpAccountCancel': 'false',
                'raw': '1519101113398',
                'secret': 'kot+b9DmI8dUebDh4utqdbDr+wWLZt+Y7X8BIxVbgCkDcGpqw1Af669dE7PPb35yenhq7p4EnXZLlMD1HnHMGZbLFyMZiwNjsD29hW+qhLgMMUv0cFu50auJVQEI+0ZS2LQruJagOKnjqTV6HPQGFANDb+Vfrslt6Czz2YS/kB4L4s2HRajAc/ZdsFmh8qglFwKGoWfEFYrqqDLSYr1OdzapV+VifQ2j8K4Q/MobT/E0nUOrbj/IYN5PmY4Xfl0qXhM9uwQ3i6VbUtv5u1kh9QIgNpwVqX0Z3ifUjyTXi66CnanyXjzWU/XXPVzN050HD1FZVUyRhXdA09anE5Mn5Q==',
                }
        #print(data)
        self.sig_data.update(data)
        #print(self.sig_data)


    def message_authentication_code(self):
        aucode_url = "https://apissl.ksapisrv.com/rest/n/user/requestMobileCode?"
        data = self.get_final_data(self.get_sig_data_aucode(str(self.phone)))
        result = requests.post(url=aucode_url + self.url_tail, data=data)
        print(result.text)

    def get_login_token(self):
        mobile_verifycode = "https://apissl.ksapisrv.com/rest/n/user/login/mobileVerifyCode?"
        code = input("输入短信验证码：")
        data = self.get_final_data(self.get_sig_data_verify(code))
        print("===================")
        print(data)

        result = requests.post(url=mobile_verifycode+self.url_tail,data=data)
        print(result.text)
        if("kuaishou.api_st" not in result.text):
            tokenLoginInfo =  result.json()['tokenLoginInfo']
            loginType = tokenLoginInfo['loginType']
            smsCode = tokenLoginInfo['smsCode']
            loginToken = tokenLoginInfo['loginToken']
            loginToken, smsCode, loginType = self.get_token(loginType, smsCode, loginToken)
            return loginToken,smsCode,loginType
        else:
            api_client_salt = result.json()['token_client_salt']
            api_st = result.json()['kuaishou.api_st']
            token = result.json()['token']
            return api_client_salt,api_st,token


    def get_token(self,logintype,smscode,logintoken):
        user_login_token_url = "https://apissl.ksapisrv.com/rest/n/user/login/token?"

        #cc = "https://apissl.ksapisrv.com/rest/n/user/login/token?mod=OPPO%28OPPO%20R17%29&lon=115.569574&country_code=CN&kpn=KUAISHOU&oc=GENERIC&egid=DFP4084137FA96075CC14A391BB509C31FA50EC9D2CFCA8980AD53AFA7C8BFCF&hotfix_ver=&sh=1600&appver=6.9.2.11245&max_memory=128&isp=CMCC&browseType=1&kpf=ANDROID_PHONE&did=ANDROID_4c1d96d144ad9668&net=WIFI&app=0&ud=0&c=GENERIC&sys=ANDROID_5.1.1&sw=900&ftt=&language=zh-cn&iuid=&lat=39.001975&did_gt=1597479943975&ver=6.9"
        data = self.get_final_data(self.get_sig_data_token(logintype,smscode,logintoken))
        print(data)


        result = requests.post(url=user_login_token_url+self.url_tail,data=data)

        print(result.text)
        print(result.json())
        api_client_salt = result.json()['token_client_salt']
        api_st = result.json()['kuaishou.api_st']
        token = result.json()['token']
        return api_client_salt,api_st,token


if __name__=="__main__":
    login = GifLogin()
    login.message_authentication_code()
    api_client_salt,api_st,token = login.get_login_token()

    print(api_client_salt,api_st,token)
    f = open("login_data.txt", "w")
    f.writelines(login.phone+","+api_client_salt+","+api_st+","+token)
