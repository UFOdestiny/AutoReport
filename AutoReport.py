import os
import random
import requests
from urllib.parse import parse_qs
from config_ import User1

os.environ['no_proxy'] = '*'


class AlreadyExist(Exception):
    """ 已存在某日的出入校申请记录 """
    pass


class AutoReport(User1):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/80.0.3987.163 Safari/537.36 Edg/80.0.361.111", }

    auth_url = 'https://iaaa.pku.edu.cn/iaaa/oauthlogin.do'
    auth_url2 = 'https://portal.pku.edu.cn/portal2017/util/appSysRedir.do?appId=stuCampusExEn'
    appid = 'portal2017'
    redirUrl = "https://portal.pku.edu.cn/portal2017/ssoLogin.do"

    def __init__(self):
        super().__init__()

        self.data = None
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

    def save_first(self):
        """
        保存设置信息
        :param data:
        :return:
        """
        url_save = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/saveSqxx?sid={self.sid}&_sk={self.username}"
        self.data = self.to_json()
        try:
            res = self.post(url_save, json=self.data)
            print(res.get("msg"))
            self.row = res.get("row")
        except AlreadyExist:

            """
            如果当天已经存在申请信息，则直接上传图片与申请即可
            """
            self.get_row()
            self.data["sqbh"] = self.row
            res = self.post(url_save, json=self.data)
            print(res.get("msg"))
            self.row = res.get("row")

    def submit(self):
        """
        提交申请
        :return:
        """
        url = f"https://simso.pku.edu.cn/ssapi/stuaffair/epiApply/submitSqxx?sid={self.sid}&sqbh={self.row}&_sk={self.username}"
        resq = self.get(url, raw=False)
        print(resq.get("msg"))

    def run(self):
        self.login1()
        self.login2()
        self.get_sid()
        self.get_cookies()

        self.save_first()

        self.submit()


if __name__ == "__main__":
    AutoReport().run()
