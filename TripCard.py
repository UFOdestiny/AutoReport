from selenium import webdriver
from config import User1
import os
import time


class TripCard:
    def __init__(self,
                 jpg_path="TripCard.png",  # 行程码图片保存地址
                 executable_path='chromedriver.exe'):  # chromedriver.exe地址
        # 引入用户
        user = User1()
        files = os.listdir(user.path)
        if "TripCard.png" in files:
            file_time = os.stat(f"{user.path}/TripCard.png").st_ctime
            if (time.time() - file_time) / 3600 < 10:
                self.flag = False
                return
            else:
                self.flag = True

        self.html = f"https://tripcard.pages.dev/#{user.phone_number}&{user.route}"

        self.jpg_path = jpg_path
        self.executable_path = executable_path
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('window-size=1920x1080')

    def run(self):
        if not self.flag:
            return
        driver = webdriver.Chrome(executable_path=self.executable_path, options=self.options)
        driver.get(self.html)
        driver.execute_script("window.scrollTo(0,100)")
        driver.set_window_size(2000, 4000)
        driver.get_screenshot_as_file(self.jpg_path)
        driver.quit()


if __name__ == '__main__':
    jpg = TripCard()
    jpg.run()
