import datetime

today = (datetime.datetime.now().date()).strftime('%Y%m%d')
tomorrow = (datetime.datetime.now().date() + datetime.timedelta(days=1)).strftime('%Y%m%d')


class User:
    def __init__(self):
        self.username = ""
        self.password = ""

        self.time = tomorrow
        self.reason_out = "学业"
        self.from_location = "燕园"
        self.to_location = "校外（社会面）"
        self.gate = "南门"
        self.detailed_reason = "实习"
        self.country = "156"  # 中国
        self.province = "11"  # 北京
        self.city = "01"  # 市辖区
        self.district = "08"  # 海淀
        self.street = "学院路街道 "
        self.detailed_route = "南门-392路（海淀桥东—保福寺桥北）-财智国际大厦"
        self.email = "1976438440@qq.com"
        self.phone_number = "15964938382"
        self.campus = "燕园"
        self.dormitory = "燕园37楼"
        self.room_number = "317"

        self.route = "北京市"  # 路径

    def to_json(self):
        empty_json = {
            "sqbh": "",
            "crxqd": self.from_location,
            "crxzd": self.to_location,
            "qdbc": "",
            "zdbc": "",
            "qdxm": self.gate,
            "zdxm": "",
            "crxrq": self.time,
            "dzyx": self.email,
            "yddh": self.phone_number,
            "ssyq": self.campus,
            "ssl": self.dormitory,
            "ssfjh": self.room_number,
            "crxsy": self.reason_out,
            "crxjtsx": self.detailed_reason,
            "yqc": [],
            "yqr": [],
            "gjdqm": self.country,
            "ssdm": self.province,
            "djsm": self.city,
            "xjsm": self.district,
            "jd": self.street,
            "bcsm": "",
            "crxxdgj": self.detailed_route,
            "dfx14qrbz": "y",
            "sfyxtycj": "",
            "tjbz": "",
            "shbz": "",
            "shyj": "",
            "fxjwljs": "",
            "fxzgfxljs": "",
            "fxqzmj": "",
            "fxyczz": "",
            "lxdh": self.phone_number}

        return empty_json


class User1(User):
    def __init__(self):
        super().__init__()
        self.username = "1900016644"
        self.password = "YUDAHAIhenniu123"


class User2(User):
    def __init__(self):
        super().__init__()
        self.username = "1900016603"
        self.password = "XKLBUER2"


class User3(User):
    def __init__(self):
        super().__init__()
        self.username = "1900016630"
        self.password = "cos(60*)"


class User4(User):
    def __init__(self):
        super().__init__()
        self.username = "1900016606"
        self.password = "7u5pk8bp9vLDL"
        self.route = "北京市"


if __name__ == "__main__":
    print(tomorrow)
    print(User2().to_json())