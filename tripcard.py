from selenium import webdriver
from config2 import User1


class TripCard:
    def __init__(self,
                 jpg_path="TripCard.png",
                 executable_path='chromedriver.exe'):
        user = User1()
        self.html = f"https://tripcard.pages.dev/#{user.phone_number}&{user.route}"

        self.jpg_path = jpg_path
        self.executable_path = executable_path
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('window-size=1920x1080')

    def run(self):
        driver = webdriver.Chrome(executable_path=self.executable_path, options=self.options)
        driver.get(self.html)
        driver.execute_script("window.scrollTo(0,100)")
        driver.set_window_size(2000, 4000)
        driver.get_screenshot_as_file(self.jpg_path)
        driver.quit()


if __name__ == '__main__':
    jpg = TripCard()
    jpg.run()
