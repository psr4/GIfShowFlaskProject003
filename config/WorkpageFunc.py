from Config import config

import hashlib
import requests
from urllib import parse
import copy
import time
import urllib3
import re

class WorkpageFunc:
    def __init__(self, url):
        self.share_url = url
        configs = config()
        self.headers = configs.HEADERS
        self.sig_data = configs.SIG_DATA
        self.salt = config().SALT
        self.token_salt = configs.TOKEN_SALT

    def sig_and_headers(self,sigdata):
        sig_str = ""
        url_headers = {}
        head = list(self.headers)
        sig_key = copy.deepcopy(self.headers)
        sig_key.update(sigdata)
        key = sorted(list(sig_key))
        for i in range(0, len(key)):
            if key[i] == 'exp_tag0':
                key[i], key[i - 1] = key[i - 1], key[i]
        for i in key:
            sig_str = sig_str + i + "=" + sig_key[i]
        self.sig_str = sig_str
        head.sort()
        for i in head:
            url_headers[i] = self.headers[i]
        self.url_tail = parse.urlencode(url_headers)


    def get_sig_data_like(self):
        data_sig = copy.deepcopy(self.sig_data)
        userid, photoid, exp_tag = self.get_user_workpage_id()
        data = {
            'user_id': userid,
            'photo_id': photoid,
            'cancel': '0',
            'referer': 'ks://photo/'+userid+'/'+photoid+'/'+exp_tag+'#like',
            'exp_tag0': '',
            'exp_tag': exp_tag,
            'serverExpTag': 'feed_photo|'+photoid+'|'+userid+'|'+exp_tag,
            'expTagList': 'CgKQ2ZlZWRfcGhvdG98NTIyNzU1MzMwNTc5NDg3MTQ4NHw0MzQwNjYxMzB8MV9pLzIwMDAxMDg3MDU3MTE3MTE1MjFfZjASATE=',
            'photoinfo': '_/_',
        }
        data_sig.update(data)
        return data_sig
    def get_sig_data_comment(self):
        comment_content = 'hahahahhahahahahhahah'
        data_sig = copy.deepcopy(self.sig_data)
        userid,photoid,exp_tag = self.get_user_workpage_id()
        data = {'photo_id': photoid,
                'user_id': userid,
                'referer': 'ks://photo/{}/{}/3/{}#addcomment'.format(userid,photoid,exp_tag),
                'content': self.comment_content,
                'reply_to': '',
                'replyToCommentId': '',
                'copy': '0',
                'praiseCommentId': '0',
                }
        data_sig.update(data)
        return data_sig





    def get_sig_data_follow(self):
        data_sig = copy.deepcopy(self.sig_data)
        userid,photoid,exp_tag = self.get_user_workpage_id()
        data = {
            'touid': userid,
            'ftype': '1',
            'act_ref': userid+'_'+photoid+'_p6',
            'page_ref': '16',
            'referer': 'ks://photo/{}/{}/3/1_i/{}#follow'.format(userid,photoid,exp_tag),
            'exp_tag0': '_',
            'exp_tag': exp_tag,
            'expTagList': 'CksKRmZlZWRfcGhvdG98NTE5MjkzMTg4MzI5MDIxNDI2OXwyMDUxNjU4MjI3fDFfaS8yMDAwMTI4MjI1ODkyOTE3OTM4X2YxMDISATE=',
            'photoinfo': '_/_',
            'followSource': '0',
        }
        data_sig.update(data)
        return data_sig

    def getNsTokenSig(self, sig):
        str3 = sig + self.token_salt
        cc = bytearray(str3.encode())
        nstokensig = hashlib.sha256(bytearray(str3.encode())).hexdigest()
        return nstokensig

    def get_final_data(self,sigdata):
        self.sig_and_headers(sigdata)
        str = self.sig_str + self.salt
        m = hashlib.md5(str.encode())
        sig = m.hexdigest()
        ns_token = self.getNsTokenSig(sig)
        data = {'sig': sig,
                '__NStokensig': ns_token}
        data.update(sigdata)
        print(data)
        return data





    def get_user_workpage_id(self):
        sh_url = self.share_url
        pat = " https:\/\/v.kuaishou.com\/(.*?) "
        res = re.findall(pat, sh_url)
        url = "https://v.kuaishou.com/" + res[0]
        http = urllib3.PoolManager()
        r = http.request("GET", url, redirect=False)
        str = r.headers["Location"]
        pat1 = '&userId=(.*?)&'
        pat2 = 'hareObjectId=(.*?)&'
        exp_pat = "&et=(.*?)&"
        exp = re.findall(exp_pat, str)
        exp_tag = exp[0].replace('%2F', '/')
        print(exp_tag)
        workpage_id = ''
        web_userid = ''
        try:
            workpage_id = re.findall(pat2,str)
            print(workpage_id[0])

            web_userid = re.findall(pat1, str)
            print(web_userid[0])
        except:
            print('复制的链接没有找到作品或者作者ID')

        user_url = "https://live.kuaishou.com/m_graphql"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Cookie': 'did=web_17f679b39ff1409aa7373f131fee7e10; didv=1592816174000; clientid=3; client_key=65890b29;'
                      ' Hm_lvt_86a27b7db2c5c0ae37fee4a8a35033ee=1594447676,1594706049,1594892726,1595902429; kuaishou.live.bfb1s=9b8f70844293bed778aade6e0a8f9942; userId=1942009504;'
                      ' userId=1942009504; kuaishou.live.web_st=ChRrdWFpc2hvdS5saXZlLndlYi5zdBKgAQ01cLyQ6xvzEkK7JaZATG0yIFcgxVbTQDjCwD2vtXYKAsFUp0eYR5s4QfKBAWyaXAynKCIt1fEV6EWrTLflgZ-47V70KOl36uaXJz_2VVZypm18o7AJIFZHULqwZ2OA8XkPo0UUxWT88fzMtrQi8wtTYdKciovdRefI9XuwcDg9Foru0gtjGbCYEtvVjczONVwLzOkXpHh0XaAAqc7PN0gaEpwewD8CakIZrC7t8JEKqqml3iIgfj_W6Lqg0rsSbgx-BMP2Qv7PkCThDEqGGnF20yukNMAoBTAB; kuaishou.live.web_ph=e2bab168a06cdae3860f79ea632ac5a5d8b5; WEBLOGGER_HTTP_SEQ_ID=6226; WEBLOGGER_INCREAMENT_ID_KEY=6436',
            }
        data = {"operationName": "sensitiveUserInfoQuery", "variables": {"principalId": web_userid[0]},
                "query": "query sensitiveUserInfoQuery($principalId: String) {\n  sensitiveUserInfo(principalId: $principalId) {\n    kwaiId\n    originUserId\n    constellation\n    cityName\n    counts {\n      fan\n      follow\n      photo\n      liked\n      open\n      playback\n      private\n      __typename\n    }\n    __typename\n  }\n}\n"}

        cc = requests.post(url=user_url, headers=headers, json=data)
        jn = cc.json()
        user_id = jn["data"]["sensitiveUserInfo"]["originUserId"]
        print(user_id,workpage_id[0],exp_tag)
        return user_id,workpage_id[0],exp_tag

    def Workpagelike(self):
        like_url = 'https://apis2.ksapisrv.com/rest/photo/like?'
        data = self.get_final_data(self.get_sig_data_like())
        result = requests.post(url=like_url+self.url_tail,data=data)
        print(result.text)
        return result.text

    def Workpagefollow(self):
        data = self.get_final_data(self.get_sig_data_follow())
        follow_url = 'https://apis2.gifshow.com/rest/n/relation/follow?'
        result = requests.post(url = follow_url+self.url_tail,data=data)
        print(result.text)
        return result.text
    def Workpagecomment(self,comment):
        self.comment_content = comment
        comment_url = 'https://api3.ksapisrv.com/rest/photo/comment/add?'
        data = self.get_final_data(self.get_sig_data_comment())
        result = requests.post(url = comment_url+self.url_tail,data=data)
        print(result.text)
        return result.text





if __name__ == "__main__":
    share_url = "这是一只聪明的猫猫 https://v.kuaishou.com/899TWH 复制此消息，打开【快手】直接观看！"
    WF = WorkpageFunc(share_url)
    #WF.Workpagefollow()
    comment_con = "ahhahahahahhah"
    WF.Workpagecomment(comment_con)
    WF.Workpagelike()