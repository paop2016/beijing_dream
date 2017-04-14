import urllib.request,urllib.parse
import http.cookiejar,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import re,socket
class Downloader():
    def __init__(self):
        self.name='HP024814'
        self.password='512512'
        self.login()
    def login(self):
        if not self.login_nomal():
            self.login_authCode()
        self.alpha_get_response('http://exam.ipmph.com/learncenter/centre/myCourse.zhtml')
    def login_nomal(self):
        userInfo = {'_ZVING_METHOD': 'dologin',
                    '_ZVING_URL': '%2FLogin.jsp',
                    '_ZVING_DATA':'{"ServiceID":"exam2016","Referer":"http://exam.ipmph.com/learncenter/member/login","plat":"","AppID":"33","UserName":"%s","Password":"%s","AuthCode":""}'%(self.name,self.password),
                    '_ZVING_DATA_FORMAT':'json'
                    }
        cookie = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
        response=self.opener.open('http://sso.ipmph.com/ajax/invoke',
                                    urllib.parse.urlencode(userInfo).encode('utf-8'))
        # response =self.opener.open('http://sso.ipmph.com/Page/Index.jsp')
        response=response.read().decode('utf-8')
        if '"_ZVING_STATUS":1' in response:
            print('登入成功')
            return True
        elif '用户名或密码错误' in response:
            print('用户名或密码错误')
            return True
        elif '请填写验证码！' in response :
            print('需要验证码，正在获取..')
        else:
            print('未知错误')
            return True
    def login_authCode(self):
        self.driver = webdriver.PhantomJS()
        self.driver.get('http://sso.ipmph.com/Login.jsp?ServiceID=ipmph&Referer=http%3A%2F%2Fwww.ipmph.com%2Flogin%2Fssosync')
        name_form = self.driver.find_element_by_id('UserName')
        password_form = self.driver.find_element_by_id('Password')
        c = self.driver.find_element_by_class_name('zz-color')
        # login_button=c.find_element(By.XPATH,'./input')
        login_button = c.find_element(By.TAG_NAME, 'input')
        name_form.send_keys(self.name)
        password_form.send_keys(self.password)
        login_button.click()
        try:
            # 检验是否登入成功（10秒以内）
            # WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located([By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/ul/li[1]/a[1]']))
            # 测试方法，可能有bug
            WebDriverWait(self.driver, 3).until_not((expected_conditions.presence_of_element_located([By.ID,'UserName'])))
        # text找不到
        # c=self.driver.find_elements_by_xpath(("//a[contains(text(), ’退出’)]"));
        except TimeoutException:
            try:
                count=0
                img_element = self.driver.find_element_by_id('AuthCodeImg')
                img_url = img_element.get_attribute('src')
                while img_url == None:
                    count+=1
                    print('正在等待加载验证码:'+str(count))
                    if count==100:
                        break
                    time.sleep(.5)
                    img_url = self.driver.find_element_by_id('AuthCodeImg').get_attribute('src')
            except TimeoutException:
                print('检查网络和账号密码')
            else:
                # action=ActionChains(self.driver)
                # action.move_to_element(img_element).context_click().send_keys('i').perform()
                self.driver.save_screenshot('c://验证码图片.jpg')
                code=input('请输入验证码 >>>>')
                auth_form = self.driver.find_element_by_id('AuthCode')
                auth_form.send_keys(code)
                login_button.click()
                # WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located([By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/ul/li[1]/a[2]']))
                # except TimeoutException:
                #     WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located([By.XPATH, '//*[@id="header"]/div[2]/ul[2]/li[2]/span']))
                WebDriverWait(self.driver, 30).until_not((expected_conditions.presence_of_element_located([By.ID, 'UserName'])))
        if self.driver.current_url in ['http://www.ipmph.com/','http://sso.ipmph.com/userinfo']:
            print('登入成功')
            print(self.driver.page_source)
            # WebDriverWait(self.driver,30).until(expected_conditions.presence_of_element_located([By.XPATH,'//*[@id="headercontent"]/div[1]/span/a[1]/font']))
            # a=self.driver.find_element_by_xpath('//*[@id="headercontent"]/div[1]/span/a[1]/font')
            # print(a.text)
            # print(a.get_attribute('style'))
        else:
            print(self.driver.current_url)

        self.driver.get('http://exam.ipmph.com/learncenter/centre/myCourse.zhtml')
        cookie=self.driver.get_cookies()
        cookie_arr = [item['name'] + '=' + item['value'] for item in cookie]
        cookie_str = ';'.join(cookie_arr)
        self.headers = {'Cookie': cookie_str}
        self.driver.close()

    def down_chapters(self):
        datadic={
            '_ZVING_METHOD':'com.zving.framework.ui.control.DataListUI.doWork',
            '_ZVING_URL':'%2Flearncenter%2Fcentre%2FmyCourse.zhtml',
            '_ZVING_DATA':'{"_ZVING_METHOD":"MyCourseCentre.listbind","_ZVING_SIZE":30,"_ZVING_AUTOFILL":"true","_ZVING_PAGE":true,"_ZVING_ID":"dl1","Login":"true","UserName":"%s","BranchInnerCode":"0001","ExamType":"Ehls00","ExamTypeName":"护士执业","ContextPath":"/learncenter/","_ZVING_TAGBODY":"centre/myCourse.zhtml#958539bc66bcb70980bde274899c6962","_ZVING_PAGEINDEX":0,"_ZVING_PAGETOTAL":-1,"FDBID":"1201","CourseID":"211"}'%self.name,
            '_ZVING_DATA_FORMAT':'json'
        }
        response = self.alpha_get_response('http://exam.ipmph.com/learncenter/ajax/invoke',datadic)
        return response.read()
    def down_sections(self,chapters_ifo):
        sections_html=[]
        for chapter_ifo in chapters_ifo:
            datadic={
                '_ZVING_METHOD': 'com.zving.framework.ui.control.DataListUI.doWork',
                '_ZVING_URL': '%2Flearncenter%2Fcentre%2FmyCourseDetail.zhtml',
                '_ZVING_DATA':'{"_ZVING_METHOD":"MyCourseCentre.dl1Databind","_ZVING_SIZE":50,"_ZVING_AUTOFILL":"true","_ZVING_PAGE":true,"_ZVING_ID":"dl1","FDBID":"1201","CourseID":"211","CatalogID":"%s","Login":"true","UserName":"%s","BranchInnerCode":"0001","ExamType":"Ehls00","ExamTypeName":"护士执业","ContextPath":"/learncenter/","_ZVING_TAGBODY":"centre/myCourseDetail.zhtml#68ca8fbf77bcaabcfc6d43d8015167cc","_ZVING_PAGEINDEX":0,"_ZVING_PAGETOTAL":-1}'%(chapter_ifo[0],self.name),
                '_ZVING_DATA_FORMAT':'json'
            }
            response=self.alpha_get_response('http://exam.ipmph.com/learncenter/ajax/invoke',datadic)
            sections_html.append([chapter_ifo[1],response.read()])
        return sections_html

    def down_section_detail(self,id):
        url=self.section_url_maker(id)
        try:
            response=self.alpha_get_response(url).read()
        except OSError as e:
            print(str(e)+'奇怪异常')
            return self.alpha_get_response(url).read()
        return response
    # 根据id，返回带答案课程的url
    def section_url_maker(self,id):
        url='http://exam.ipmph.com/learncenter/MyPaperNew.paper.zaction?ID=' + id + '&referer=myPaper.zhtml'
        response=self.alpha_get_response(url)
        return 'http://exam.ipmph.com/learncenter/centre/paperDetail.zhtml?Key_Success=%s'%re.search('=.+&',response.geturl()).group()[1:-1]

    def alpha_get_response(self,url,datadic=None,try_times=5):
        try:
            if hasattr(self,'headers'):
                request=urllib.request.Request(url,headers=self.headers)
                if datadic:
                    response=urllib.request.urlopen(request,urllib.parse.urlencode(datadic).encode('utf-8'),timeout=3)
                    return response
                else:
                    response=urllib.request.urlopen(request,timeout=3)
                    return response
            else:
                if datadic:
                    response=self.opener.open(url,urllib.parse.urlencode(datadic).encode('utf-8'),timeout=3)
                    return response
                else:
                    response=self.opener.open(url,timeout=3)
                    return response
        except OSError as e:
            print(str(e)+">>>"+'剩余尝试次数：'+str(try_times-1)+'次')
            return self.alpha_get_response(url,datadic,try_times-1)