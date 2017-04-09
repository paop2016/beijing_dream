import urllib.request,urllib.parse
import http.cookiejar
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import os
from selenium.common.exceptions import NoSuchElementException
class Downloader():
    def __init__(self):
        c=0
        while True:
            a=self.login()
            c+=1
            print(c)
            if a!='http://www.ipmph.com/':
                break

        # self.login()
    def login(self):
        self.driver = webdriver.PhantomJS()
        self.driver.get('http://sso.ipmph.com/Login.jsp?ServiceID=ipmph&Referer=http%3A%2F%2Fwww.ipmph.com%2Flogin%2Fssosync')
        name_form = self.driver.find_element_by_id('UserName')
        password_form = self.driver.find_element_by_id('Password')
        c = self.driver.find_element_by_class_name('zz-color')
        # login_button=c.find_element(By.XPATH,'./input')
        login_button = c.find_element(By.TAG_NAME, 'input')
        name_form.send_keys('HP024814')
        password_form.send_keys('512512')
        login_button.click()
        # count=0
        # while True:
        #     try:
        #         a=self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/ul/li[1]/a[1]')
        #     except NoSuchElementException:
        #         count+=1
        #         print(count)
        #     else:
        #         break
        #     count+=1
        #     print(count)
        #     if count==20:
        #         break
        WebDriverWait(self.driver, 1000).until(expected_conditions.presence_of_element_located([By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/ul/li[1]/a[1]']))
        # a = self.driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[2]/ul/li[1]/a[1]')
        # b = self.driver.find_element_by_xpath('/ html / body / div[1] / div[1] / div / div[1]')
        # text找不到
        # c=self.driver.find_elements_by_xpath(("//a[contains(text(), ’退出’)]"));
        a=self.driver.current_url
        print(a)
        self.driver.close()
        return a
        # print(self.driver.page_source)
        # print(c)

        # self.driver.get('http://exam.ipmph.com/learncenter/centre/chapterTraining.zhtml')
        # print(self.driver.current_url)
        # self.driver.close()
        # c=self.driver.driverfind_element_by_class_name('zz-color')
            # login_button=c.find_element(By.TAG_NAME,'input')
            # # login_button=c.find_element(By.XPATH,'./input')
            # login_button.click()
            # # 显示等待
            # # self.driver.implicitly_wait(100)
            # # 隐式等待
            # # e=WebDriverWait(self.driver,30).until(expected_conditions.presence_of_element_located([By.XPATH,"//img[@id='AuthCodeImg']/style"] ))
            # img_url=self.driver.find_element_by_id('AuthCodeImg').get_attribute('src')
            # while img_url==None:
            #     self.driver.implicitly_wait(5)
            #     img_url = self.driver.find_element_by_id('AuthCodeImg').get_attribute('src')
            # print(self.driver.current_url)
            #
            # # cookie_arr=[item['name']+'='+item['value'] for item in self.driver.get_cookies()]
            # # cookie_str=';'.join(item for item in cookie_arr)
            #
            # # self.driver.add_cookie()
            # response=urllib.request.urlopen(img_url).read()
            # with open('c:\\test.jpg','wb') as f:
            #     f.write(response)
            # code=input('输入验证码>>>')
            # # 填写验证码
            # # print(cookie_str)
            # # cookie_strcookie_str
            # auth_form = self.driver.find_element_by_id('AuthCode')
            # auth_form.send_keys(code)
            # login_button.click()
            # # self.driver.implicitly_wait(100)
            # WebDriverWait(self.driver,5000).until(expected_conditions.presence_of_element_located([By.CLASS_NAME,'wrap100 topBg']))
            # print(self.driver.current_url)
            # # print(self.driver.page_source)
    def login_old(self):
        # 简单登入表单
        # userData={
        #           "UserName": "HP024814",
        #           "Password": "512512"
        #           }

        # 复杂登入表单
        userData={
                  '_ZVING_METHOD':'dologin',
                  '_ZVING_URL':'%2FdoLogin.jsp',
                  '_ZVING_DATA':'{"ServiceID":"ipmph","Referer":"http://www.ipmph.com/login/ssosync","plat":"","AppID":"26","UserName":"HP024814","Password":"512512","AuthCode":""}',
                  '_ZVING_DATA_FORMAT':'json'
                  }

        # # 主登入接口,登入过多会要求验证码
        url='http://sso.ipmph.com/ajax/invoke'
        # 未知可用接口
        # url='http://sso.ipmph.com/doLogin?Referer=http%3A%2F%2Fexam.ipmph.com%2F'

        # 学术登入接口，可用
        # url='http://sso.ipmph.com/doLogin?ServiceID=medical&Referer=http%3A%2F%2Fmedbooks.ipmph.com%2Fmedical%2Fmedbooks%2Findex.zhtml'

        cookie=http.cookiejar.CookieJar()
        self.opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
        # self.opener = urllib.request.build_opener()
        response=self.opener.open(url,urllib.parse.urlencode(userData).encode('utf-8'))
        if response.geturl()=='http://sso.ipmph.com/ajax/invoke':
            self.driver.get('http://sso.ipmph.com/Login.jsp?ServiceID=ipmph&Referer=http%3A%2F%2Fwww.ipmph.com%2Flogin%2Fssosync')
            name_form=self.driver.find_element_by_id('UserName')
            password_form=self.driver.find_element_by_id('Password')
            name_form.send_keys('HP024814')
            password_form.send_keys('512512')

            c=self.driver.find_element_by_class_name('zz-color')
            login_button=c.find_element(By.TAG_NAME,'input')
            # login_button=c.find_element(By.XPATH,'./input')
            login_button.click()
            # 显示等待
            # self.driver.implicitly_wait(100)
            # 隐式等待
            # e=WebDriverWait(self.driver,30).until(expected_conditions.presence_of_element_located([By.XPATH,"//img[@id='AuthCodeImg']/style"] ))
            img_url=self.driver.find_element_by_id('AuthCodeImg').get_attribute('src')
            while img_url==None:
                self.driver.implicitly_wait(5)
                img_url = self.driver.find_element_by_id('AuthCodeImg').get_attribute('src')
            print(self.driver.current_url)

            # cookie_arr=[item['name']+'='+item['value'] for item in self.driver.get_cookies()]
            # cookie_str=';'.join(item for item in cookie_arr)

            # self.driver.add_cookie()
            response=urllib.request.urlopen(img_url).read()
            with open('c:\\test.jpg','wb') as f:
                f.write(response)
            code=input('输入验证码>>>')
            # 填写验证码
            # print(cookie_str)
            # cookie_strcookie_str
            auth_form = self.driver.find_element_by_id('AuthCode')
            auth_form.send_keys(code)
            login_button.click()
            # self.driver.implicitly_wait(100)
            WebDriverWait(self.driver,5000).until(expected_conditions.presence_of_element_located([By.CLASS_NAME,'wrap100 topBg']))
            print(self.driver.current_url)
            # print(self.driver.page_source)

    def a(self):
        # 我的课堂
        opener = urllib.request.build_opener()
        my_headers = {
            'cookie': '__utmz=243059712.1491550009.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);__utmc=243059712;__utmb=243059712.1.10.1491550009;__utma=243059712.1993462675.1491550009.1491550009.1491550009.1;__utmt=1;Hm_lpvt_ec31b23a3a54fb0e85df69fc93bd5de9=1491550009;Hm_lvt_ec31b23a3a54fb0e85df69fc93bd5de9=1491537875,1491540549,1491540798,1491550009;route=0309f67242e2cf26e09d12032ecc3877;JSESSIONID=B7194EA2E69215DF318EDDD08A6E187A.jvm3'}
        userData = {
            '_ZVING_METHOD': 'dologin',
            '_ZVING_URL': '%2FdoLogin.jsp',
            '_ZVING_DATA': '{"ServiceID":"ipmph","Referer":"http://www.ipmph.com/login/ssosync","plat":"","AppID":"26","UserName":"HP024814","Password":"512512",'
                           '"AuthCode":"7ybmk"}',
            '_ZVING_DATA_FORMAT': 'json'
        }
        my_request = urllib.request.Request('http://sso.ipmph.com/ajax/invoke', headers=my_headers)
        response = opener.open(my_request, urllib.parse.urlencode(userData).encode('utf-8'))
        html = response.read().decode('utf-8')
        print(html)
        print(response.geturl())


        pass