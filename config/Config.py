class config:
    def __init__(self):
        self.HEADERS = {'mod': 'OPPO(OPPO R17)',
                        'lon': '115.569574',
                        'country_code': 'CN',
                        'kpn': 'KUAISHOU',
                        'oc': 'GENERIC',
                        'egid': 'DFP4084137FA96075CC14A391BB509C31FA50EC9D2CFCA8980AD53AFA7C8BFCF',
                        'hotfix_ver': '',
                        'sh': '1600',
                        'appver': '6.9.2.11245',
                        'max_memory': '128',
                        'isp': 'CMCC',
                        'browseType': '1',
                        'kpf': 'ANDROID_PHONE',
                        'did': 'ANDROID_4c1d96d144ad9668',
                        'net': 'WIFI',
                        'app': '0',
                        'ud': '0',
                        'c': 'GENERIC',
                        'sys': 'ANDROID_5.1.1',
                        'sw': '900',
                        'ftt': '',
                        'language': 'zh-cn',
                        'iuid': '',
                        'lat': '39.001975',
                        'did_gt': '1597479943975',
                        'ver': '6.9',
                        }
        path = "login_data.txt"
        f = open(path, "r")
        data = f.read()
        try:
            log = data.split(",")
            log[2]
        except:
            log = ["","","",""]
        print(log)
        self.SALT = '382700b563f4'
        self.TOKEN_SALT = log[1]
        self.PHONE_NUMBER = "18202697225"

        self.SIG_DATA = {

            'kuaishou.api_st': log[2],
            'token': log[3],
            'client_key': '3c2cd3f3',
            'os': 'android',

        }
if __name__ == "__main__":
    cc = config()