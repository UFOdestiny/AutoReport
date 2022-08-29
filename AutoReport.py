import random
from urllib.parse import parse_qs
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from tripcard import TripCard

from config import User1


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
        """
        请求函数
        :param method: GET/POST
        :param url:
        :param raw: False → json
        :param headers:
        :param kwargs:
        :return:
        """
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
        """
        POST
        :param url:
        :param data:
        :param kwargs:
        :return:
        """
        return self.request('POST', url, data=data, **kwargs)

    def get(self, url, params=None, raw=True, **kwargs):
        """
        GET
        :param url:
        :param params:
        :param raw:
        :param kwargs:
        :return:
        """
        return self.request('GET', url, params=params, raw=raw, **kwargs)

    def login1(self):
        """
        第一次登陆，获取token1
        :return:
        """
        data = {'appid': self.appid,
                'userName': self.username,
                'password': self.password,
                'redirUrl': self.redirUrl,
                'otpCode': ""}

        resp_json = self.post(self.auth_url, data=data)
        self.token1 = resp_json.get('token')

    def login2(self):
        """
        第二次登陆，获取token2，后续都使用token2
        :return:
        """
        self.get(self.redirUrl, params={'rand': random.random(), 'token': self.token1})
        resp_json = self.get(self.auth_url2)
        self.token2 = parse_qs(resp_json.url)['token'][0]

    def get_sid(self):
        """
        获取sid
        :return:
        """
        url_sid = f'https://simso.pku.edu.cn/ssapi/simsoLogin?token={self.token2}'
        self.sid = self.get(url_sid, raw=False).get("sid")

    def get_cookies(self):
        """
        生成cookie
        :return:
        """
        url_cookies = f'https://simso.pku.edu.cn/pages/sadEpidemicAccess.html?_sk={self.username}#/epiAccessHome'
        self.get(url_cookies)

    def get_row(self):
        """
        在已经有当天保存信息的情况下，获取最新的保存记录号
        :return:
        """
        url_row = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/getSqxxHis?sid={self.sid}&_sk={self.username}&pageNum=1"
        resq = self.get(url_row, raw=False)
        self.row = resq.get("row")[0]["sqbh"]

    def save_first(self, data):
        """
        保存设置信息
        :param data:
        :return:
        """
        url_save = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/saveSqxx?sid={self.sid}&_sk={self.username}"
        try:
            resq = self.post(url_save, json=data)
            print(resq.get("msg"))
            self.row = resq.get("row")
        except AlreadyExist:
            """
            如果当天已经存在申请信息，则直接上传图片与申请即可
            """
            self.get_row()

    def upload_img(self):
        """
        上传行程码图片
        :return:
        """
        url_img = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/uploadZmcl?sid={self.sid}&_sk={self.username}"
        file_payload = {"cldms": "xcm",
                        'files': ('TripCard.png', open('TripCard.png', 'rb'), 'image/png'),
                        "sqbh": self.row}

        header_img = self.headers
        data = MultipartEncoder(file_payload)
        header_img['Content-Type'] = data.content_type
        self.post(url_img, data=data, headers=header_img)

    def submit(self):
        """
        提交申请
        :return:
        """
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
        """
        执行
        :param user: 用户类
        """
        TripCard().run()  # 获取模拟行程码

        u = user()
        simso = AutoReport(u.username, u.password)
        simso.run(u.to_json())


if __name__ == "__main__":
    Execute(User1)
