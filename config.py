import datetime

today = (datetime.datetime.now().date()).strftime('%Y%m%d')
tomorrow = (datetime.datetime.now().date() + datetime.timedelta(days=1)).strftime('%Y%m%d')


class User:
    username = ""
    password = ""

    time = tomorrow
    reason_out = "学业"
    from_location = "燕园"
    to_location = "校外（社会面）"
    gate = "南门"
    detailed_reason = "吃饭"
    country = "156"  # 中国
    province = "11"  # 北京
    city = "01"  # 市辖区
    district = "08"  # 海淀
    street = "   "
    detailed_route = "   "
    email = "0111@qq.com"
    phone_number = "111"
    campus = "燕园"
    dormitory = "燕园111楼"
    room_number = "111"

    route = "北京市"  # 路径

    path = ""

    def to_json(self):
        return {
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
            "lxdh": self.phone_number,
            "djrq": "20220823",
            "djsjbz": "y",
        }


class User1(User):
    def __init__(self):
        self.username = "1"
        self.password = "1"
        self.route = "1"


class User2(User):
    def __init__(self):
        self.username = "1"
        self.password = "1"


class User3(User):
    def __init__(self):
        super().__init__()
        self.username = "1"
        self.password = "1"


class User4(User):
    def __init__(self):
        super().__init__()
        self.username = "1"
        self.password = "1"
        self.route = "1"


if __name__ == "__main__":
    print(tomorrow)
    print(User2().to_json())
