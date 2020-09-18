import copy

import requests
import hashlib
from urllib import parse
from Config import config

class SearchWorkpage:
    def __init__(self,keyword,pcursor=0):

        self.pcursor = pcursor
        configs = config()
        self.headers = configs.HEADERS
        self.sig_data = configs.SIG_DATA
        self.sig_data.update({'keyword': keyword})
        self.salt = config().SALT

    def sig_and_headers(self,sig):
        sig_str = ""
        url_headers = {}
        head = list(self.headers)
        sig_key = self.headers
        sig_key.update(sig)
        for i in sorted(list(sig_key)):
            sig_str = sig_str + i + "=" + sig_key[i]
        head.sort()
        for i in head:
            url_headers[i] = self.headers[i]
        self.url_tail = parse.urlencode(url_headers)
        return sig_str
    def users_data_process(self,result):
        result_list = []
        #print("解析函数")
        for data in result['feeds']:
            #print(data)
            try:
                puretitle = data['pureTitle']
            except:
                puretitle = "空"
            user_name = data['user_name']
            serverexptag = data['serverExpTag']
            work_url = data['main_mv_urls'][0]['url']
            re_dict = {"user_name":user_name,"puretitle":puretitle,"serverexptag":serverexptag,"work_url":work_url}
            result_list.append(re_dict)
            # #print(puretitle)
            # #print(user_name)
            # #print(serverexptag)
            # #print(work_url)
        return str(result_list)


    def get_ussid(self,sig):
        data = copy.deepcopy(sig)
        sig_str = self.sig_and_headers(data)
        salt = '382700b563f4'
        str = sig_str + salt
        m = hashlib.md5(str.encode())
        sig = m.hexdigest()
        ##print(sig)
        data.update({"sig":sig})
        workpage_url_hair = "http://apissl.gifshow.com/rest/n/search/feed?"
        result = requests.post(url=workpage_url_hair + self.url_tail, data=data)
        result = result.json()
        ##print(result)
        self.ussid = result['ussid']


    def search_workpage_request(self,sig):
        data = copy.deepcopy(sig)
        sig_str = self.sig_and_headers(data)
        salt = '382700b563f4'
        str = sig_str + salt
        m = hashlib.md5(str.encode())
        sig = m.hexdigest()
        #print(sig)
        data.update({"sig":sig})
        workpage_url_hair = "http://apissl.gifshow.com/rest/n/search/feed?"
        result = requests.post(url=workpage_url_hair + self.url_tail, data=data)
        result = result.json()
        serverexptag = self.users_data_process(result)
        return  serverexptag


    def search_workpage(self,sig):
        for page in range(0, self.pcursor + 1):
            #print(page)
            if (page == 0):
                self.get_ussid(sig)
                yield self.search_workpage_request(sig)
            else:
                users_follow_data = {'pcursor': str(page),
                                     'ussid': self.ussid,
                                     }
                sig_tmp = copy.deepcopy(sig)
                sig_tmp.update(users_follow_data)
                yield self.search_workpage_request(sig_tmp)


if __name__ == "__main__":
    SW = SearchWorkpage("小司机",5)
    SW.search_workpage(SW.sig_data)

