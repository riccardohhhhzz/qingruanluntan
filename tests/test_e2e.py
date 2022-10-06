import logging
import sys
import time
import unittest

import kthread
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys

from app import create_app, db
from app.models.model import User
from app.utils.jwt import encrypt_password

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None


log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class SeleniumTestCase(unittest.TestCase):
    client: WebDriver

    @classmethod
    def setUpClass(cls):
        # start Chrome
        options = webdriver.ChromeOptions()
        # options.add_argument('headless')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # You need to change this to your actual binary path.
        options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
        # You need to change this to your actual web driver path.
        cls.client = webdriver.Chrome(
            'C:\Program Files\Google\Chrome\Application\chromedriver.exe', chrome_options=options)

        # create the application
        cls.app = create_app('test')
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # create the database and populate with some fake data
        db.drop_all()
        db.create_all()
        me = User(username="test", password=encrypt_password(str("test")), nickname="test",
                  mobile="+86.123456789012", magic_number=0, url="https://baidu.com")
        db.session.add(me)
        db.session.commit()

        # start the Flask server in a thread
        cls.server_thread = kthread.KThread(target=cls.app.run,
                                            kwargs={'debug': False})
        cls.server_thread.start()

        # give the server a second to ensure it is up
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

        # remove application context
        cls.app_context.pop()
        cls.server_thread.kill()

        # destroy database
        db.session.remove()
        db.drop_all()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_web(self):
        """
        EXAMPLE: 使用测试用户进行登录
        """
        self.client.get('http://127.0.0.1:5000')
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/a").click()
        self.client.find_element_by_id('username').send_keys('test')
        self.client.find_element_by_id('password').send_keys('test')
        self.client.find_element_by_xpath(
            '//*[@id="root"]/div/div[3]/div/button').click()

        """
        TODO: 登录后发帖，发帖标题为：Hello World，发帖内容为：你好！
        """
        time.sleep(1)
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/div[3]//*[@class='MuiButtonGroup-root']/a").click()
        time.sleep(1)
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/div[3]//*[@class='MuiInputBase-input MuiInput-input']").send_keys('Hello World')
        time.sleep(1)
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[2]//textarea").send_keys('你好！')
        time.sleep(1)
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[3]/button").click()
        """
        TODO: 更新帖子标题为：Hello World！，帖子内容为：你好。
        """
        time.sleep(1)
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div[2]/div[2]/span[2]/span/a[1]").click()
        time.sleep(1)
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/div[3]//*[@class='MuiInputBase-input MuiInput-input']").send_keys('!')
        time.sleep(1)
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[2]//textarea").send_keys(Keys.BACK_SPACE+'。')
        time.sleep(1)
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[3]/button").click()

        """
        TODO: 回复刚才的帖子，回复内容为：你好！
        """
        time.sleep(1)
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div[2]/div[2]/span[2]/span/a[2]").click()
        time.sleep(1)
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[2]//textarea").send_keys('你好！')
        time.sleep(1)
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div/div[3]/button").click()
        """
        TODO: 退出登录
        """
        time.sleep(1)
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/header/div/span/a").click()
        time.sleep(1)
        self.client.find_element_by_xpath(
            "//*[@id='root']/div/div[3]/div/div[6]/button").click()
        time.sleep(2)

if __name__ == '__main__':
    unittest.main()
