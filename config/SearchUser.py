import requests
import hashlib
from urllib import parse
import copy

from Config import config
class SearchUser:

    def __init__(self, keyword):
        self.keyword = keyword
        configs = config()

        self.pcursor = "0"
        self.headers = configs.HEADERS
        search_data = {
            'keyword': keyword,
        }
        self.sig_data = configs.SIG_DATA
        self.sig_data.update(search_data)

    def sig_and_headers(self,sig_data):
        sig_data = copy.deepcopy(sig_data)
        print("1111111111111")
        print(sig_data)
        sig_str = ""
        url_headers = {}
        head = list(self.headers)
        sig_key = copy.deepcopy(self.headers)
        sig_key.update(sig_data)
        print()
        for i in sorted(list(sig_key)):
            sig_str = sig_str + i + "=" + sig_key[i]

        self.sig_str = sig_str
        print('<<<<<<')
        print(sig_key)
        head.sort()
        for i in head:
            url_headers[i] = self.headers[i]
        self.url_tail = parse.urlencode(url_headers)
        print(self.url_tail)

    def search_user(self):
        users_url_hair = 'https://apissl.ksapisrv.com/rest/n/search/user?'
        workpage_url_hair = "https://apikqcc2.ksapisrv.com/rest/n/search/new?"

        salt = '382700b563f4'
        str = self.sig_str + salt

        m = hashlib.md5(str.encode())
        print("22222222222222222222222")
        print(self.sig_str)
        sig = m.hexdigest()
        data = copy.deepcopy(self.sig_data)
        sig ={'sig':sig}
        data.update(sig)

        if(self.pcursor == "0"):
            pass
        else:
            data.update(self.users_follow_data)
        print(data)
        result = requests.post(url=users_url_hair + self.url_tail, data=data)
        self.result = result.json()

    def follow_up_users_search(self, pcursor):
        self.pcursor = str(pcursor)
        print("第多少页：",str(pcursor))
        self.users_follow_data = {'pcursor': pcursor,
                             'ussid': self.ussid,
                             }
        #print(self.ussid)
        sig_data = copy.deepcopy(self.sig_data)
        sig_data.update(self.users_follow_data)
        print(">>>>>")
        return sig_data


    def users_data_process(self):

        data_json = self.result
        print(data_json)
        users = data_json['users']
        self.ussid = data_json['ussid']

        print(data_json['ussid'])
        for user in users:
            headurl = user["headurl"]
            fansCount = user['fansCount']
            try:
                kwaiId = user['kwaiId']
            except:
                kwaiId = ""
            user_id = user['user_id']
            user_name = user['user_name']
            user_sex = user['user_sex']
            user_text = user['user_text']
            #print(headurl, fansCount, kwaiId, user_id, user_name, user_text)


if __name__ == '__main__':

    search = SearchUser("老司机")
    search.sig_and_headers(search.sig_data)
    search.search_user()
    search.users_data_process()

    num = 1
    while True:
        next = input("是否需要下一页(0不需要，1需要)：")
        if(next=="1"):
            sig_data = search.follow_up_users_search(str(num))
            search.sig_and_headers(sig_data)
            search.search_user()
            search.users_data_process()
            num = num+1
