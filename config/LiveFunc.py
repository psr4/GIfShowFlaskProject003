from Config import config

import hashlib
import requests
from urllib import parse
import copy
import time
import urllib3


class LiveFunc:
    def __init__(self, url):
        self.url = url
        configs = config()
        self.headers = configs.HEADERS
        print(type(self.headers))
        self.sig_data = configs.SIG_DATA
        self.salt = config().SALT
        self.token_salt = configs.TOKEN_SALT


    # 通过分享链接拿到直播间数据
    def get_param(self):
        http = urllib3.PoolManager()
        r = http.request("GET", self.url, redirect=False)
        str = r.headers["Location"]
        author = roomid = ""
        list1 = str.split("&")
        for i in list1:
            list2 = i.split("=")
            # print(list2)
            if list2[0] == "userId":
                author = list2[1]
            if list2[0] == "shareObjectId":
                roomid = list2[1]
                self.liveStreamId = roomid
        print(author, roomid)
        return author, roomid

    # 加入sig验证的（进入直播间）data

    def get_sig_data_startlive(self):
        data_sig = copy.deepcopy(self.sig_data)
        author, roomid = self.get_param()
        data = {
            'author': author,
            'exp_tag': '1_a/0_unknown0',
            'source': '0',
            'serverExpTag': 'feed_live|' + roomid + '|' + author + '|1_a/0_unknown0',
            'tfcOpOrderList': '["1593316233958408_1942009504_1942009504_"]'

        }
        data_sig.update(data)
        return data_sig

    # 加入sig验证的（点亮红心）data
    def get_sig_data_likelive(self):
        data_sig = copy.deepcopy(self.sig_data)


        author, roomid = self.get_param()
        data = {'liveStreamId': self.liveStreamId,
                'count': '3',
                'intervalMillis': '2000',
                }
        data_sig.update(data)
        return  data_sig

    # 加入sig验证的（评论）data
    def get_sig_data_commentlive(self,content):
        author, roomid = self.get_param()
        data_sig = copy.deepcopy(self.sig_data)
        print('++++++++++')
        print(data_sig)

        data = {'liveStreamId': self.liveStreamId,
                'content': content,
                'copied': 'false',
                }
        data_sig.update(data)
        print(data_sig)
        return  data_sig

    # 对data和headers做排序
    def sig_and_headers(self,sigdata):
        sig_str = ""
        url_headers = {}
        head = list(self.headers)
        sig_key = copy.deepcopy(self.headers)
        print('----------')
        print(sigdata)
        sig_key.update(sigdata)
        for i in sorted(list(sig_key)):
            sig_str = sig_str + i + "=" + sig_key[i]
        self.sig_str = sig_str
        print(self.sig_str)
        head.sort()
        for i in head:
            url_headers[i] = self.headers[i]
        self.url_tail = parse.urlencode(url_headers)

    # 获取NsTokenSig
    def getNsTokenSig(self, sig):
        str3 = sig + self.token_salt
        cc = bytearray(str3.encode())
        nstokensig = hashlib.sha256(bytearray(str3.encode())).hexdigest()
        return nstokensig

    def get_final_data(self, sigdata):

        self.sig_and_headers(sigdata)
        print("sig_data====")
        print(sigdata)
        str = self.sig_str + self.salt
        print(str)
        m = hashlib.md5(str.encode())
        sig = m.hexdigest()
        ns_token = self.getNsTokenSig(sig)
        data = {'sig': sig,
                '__NStokensig': ns_token}
        data.update(sigdata)
        print(data)
        return data

    # 请求进入直播间
    def startplay(self):
        startplay_url = "https://apikqcc2.ksapisrv.com/rest/n/live/startPlay/v2?"
        data = self.get_final_data(self.get_sig_data_startlive())
        result = requests.post(url=startplay_url + self.url_tail, data=data)
        rejs = result.json()
        result = rejs["result"]
        print(">>>>>>>>>>>>")
        print(result)
        return result

    def livelike(self):
        livelike_url = "https://api3.gifshow.com/rest/n/live/like?"
        data = self.get_final_data(self.get_sig_data_likelive())
        result = requests.post(url=livelike_url + self.url_tail, data=data)
        print(result.text)

    def livecomment(self):
        livecomment_url = "https://api3.gifshow.com/rest/n/live/comment?"
        data = self.get_final_data(self.get_sig_data_commentlive("haohaoahaohao"))
        print("评论data======")
        print(data)
        result = requests.post(url=livecomment_url + self.url_tail, data=data)
        print(result.text)

if __name__ == "__mian__":
    gifshow = LiveFunc("https://v.kuaishou.com/95E8PD")

    #gifshow.startplay()

    gifshow.livecomment()

    # for i in range(1001):
    #     gifshow.livelike()
    #     time.sleep(1)
