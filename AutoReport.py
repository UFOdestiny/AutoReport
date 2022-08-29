import random
from urllib.parse import parse_qs
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from tripcard import TripCard

# from config2 import User1
from config2 import User1


class AlreadyExist(Exception):
    """ 已存在某日的出入校申请记录 """
    pass


class AutoReport:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.111", }

    auth_url = 'https://iaaa.pku.edu.cn/iaaa/oauthlogin.do'
    auth_url2 = 'https://portal.pku.edu.cn/portal2017/util/appSysRedir.do?appId=stuCampusExEn'
    appid = 'portal2017'
    redirUrl = "https://portal.pku.edu.cn/portal2017/ssoLogin.do"

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.token1 = None
        self.token2 = None

        self.sid = None
        self.row = None

        self.session = requests.session()
        self.session.trust_env = False

    def request(self, method, url, raw=False, headers=None, **kwargs):
        if not headers:
            headers = self.headers

        resp = self.session.request(method, url, headers=headers, **kwargs)
        if not resp.ok:
            raise Exception("error in resp.ok")
        if raw:
            return resp
        resp_json = resp.json()
        if not resp_json.get('success'):
            msg = resp_json.get("msg")
            if "已存在" in msg:
                raise AlreadyExist
            raise Exception(msg)

        return resp_json

    def post(self, url, data=None, **kwargs):
        return self.request('POST', url, data=data, **kwargs)

    def get(self, url, params=None, raw=True, **kwargs):
        return self.request('GET', url, params=params, raw=raw, **kwargs)

    def login1(self):
        data = {'appid': self.appid,
                'userName': self.username,
                'password': self.password,
                'redirUrl': self.redirUrl,
                'otpCode': ""}

        resp_json = self.post(self.auth_url, data=data)
        self.token1 = resp_json.get('token')

    def login2(self):
        self.get(self.redirUrl, params={'rand': random.random(), 'token': self.token1})
        resp_json = self.get(self.auth_url2)
        self.token2 = parse_qs(resp_json.url)['token'][0]

    def get_sid(self):
        url_sid = f'https://simso.pku.edu.cn/ssapi/simsoLogin?token={self.token2}'
        self.sid = self.get(url_sid, raw=False).get("sid")

    def get_cookies(self):
        url_cookies = f'https://simso.pku.edu.cn/pages/sadEpidemicAccess.html?_sk={self.username}#/epiAccessHome'
        self.get(url_cookies)

    def get_row(self):
        url_row = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/getSqxxHis?sid={self.sid}&_sk={self.username}&pageNum=1"
        resq = self.get(url_row, raw=False)
        self.row = resq.get("row")[0]["sqbh"]

    def save_first(self, data):
        url_save = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/saveSqxx?sid={self.sid}&_sk={self.username}"
        try:
            resq = self.post(url_save, json=data)
            print(resq.get("msg"))
            self.row = resq.get("row")
        except AlreadyExist:
            self.get_row()

    def upload_img(self):
        url_img = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/uploadZmcl?sid={self.sid}&_sk={self.username}"
        file_payload = {"cldms": "xcm",
                        'files': ('TripCard.png', open('TripCard.png', 'rb'), 'image/png'),
                        "sqbh": self.row}

        header_img = self.headers
        m = MultipartEncoder(file_payload)
        header_img['Content-Type'] = m.content_type
        self.post(url_img, data=m, headers=header_img)

    def submit(self):
        url_submit = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/submitSqxx?sid={self.sid}&sqbh={self.row}&_sk={self.username}"
        resq = self.get(url_submit, raw=False)
        print(resq.get("msg"))

    def run(self, data):
        self.login1()
        self.login2()
        self.get_sid()
        self.get_cookies()

        self.save_first(data)
        self.upload_img()
        self.submit()


class Execute:
    def __init__(self, user):
        TripCard().run()

        u = user()
        simso = AutoReport(u.username, u.password)
        simso.run(u.to_json())


if __name__ == "__main__":
    Execute(User1)
