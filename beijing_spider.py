import os
from beijing_manager import Manager
from beijing_downloader import Downloader
from beijing_parser import Parser
from beijing_outputer import Outputter
import threading,multiprocessing

from urllib import request,parse
import urllib
class Spider():
    def __init__(self):
        self.manager=Manager()
        self.downloader=Downloader()
        self.parser=Parser()
        self.outputter=Outputter('/users/tong/desktop/我的课程')
    def prepare_sections(self):
        chapters_ifo=self.parser.parse_chapters(self.downloader.down_chapters())
        self.manager.save_sections(self.parser.parse_sections(self.downloader.down_sections(chapters_ifo)))
    def main(self):
        while True:
            # 获取一个未爬取的课程信息
            # 格式为字典'_id' 'chapter_name' 'section_name' 'status'
            section=self.manager.get_one_sectionDic()
            if not section:
                break
            print(section)
            # 爬取到该课程的HTML
            html=self.downloader.down_section_detail(section['_id'])
            # 解析，返回无答案（content[0]）和有答案两种题库（content[1]）
            content=self.parser.parse_section_detail(html)
            self.outputter.write_file(section,content)
    def multi_thread(self):
        threads=[]
        for _ in range(2):
            thread=threading.Thread(target=self.main())
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
    def multi_process(self):
        processes=[]
        for _ in range(7):
            process=multiprocessing.Process(target=self.multi_thread())
            processes.append(process)
            process.start()
        for process in processes:
            process.join()
def reorganize_to_one_file():
    os.chdir('/users/tong/desktop/我的课程')
    data = ['第一节','第一、', '第二节','第二、', '第三节', '第三、','第四节', '第四、','第五节', '第五、','第六节','第六、', '第七节','第七、',
                '第八节','第八、', '第九节', '第九、','第十节','第十、', '第十一节','第十一、', '第十二节', '第十二、','第十三节','第十三、',
                '第十四节','第十四、' ,'第十五节', '第十五、','第十六节','第十六、', '第十七节', '第十七、','第十八节','第十八、','第十九节','第十九、',
                '第二十节','第二十、', '第二十一节','第二十一、', '第二十二节', '第二十二、','第二十三节', '第二十三、','第二十四节','第二十四、', "附："]
    for file in os.listdir():
        if file=='.DS_Store':
            continue
        writeFlag = False
        os.chdir(file)
        file_list=os.listdir()
        # print(file_list)
        num=0
        arr=[]
        for reg in data:
            for doc in file_list:
                # print(file + '>>>' + doc)
                if reg in doc:
                    arr.append(doc)
                    num+=1
                    writeFlag=True
                    if '答案' in doc:
                        try:
                            with open('*'+file+'(答案).doc','a') as t_file,open(doc) as f:
                                sectionName = doc.replace('【答案】', '-').replace('.doc', '\n')
                                if sectionName[0]=='-':
                                    sectionName=sectionName[1:]
                                t_file.write(sectionName)
                                t_file.write(f.read())
                        except Exception as e:
                            print(str(e) + '>>>>' + doc)
                    else:
                        try:
                            with open('*'+file+'.doc', 'a') as t_file, open(doc) as f:
                                sectionName = doc.replace('.doc', '\n')
                                t_file.write(sectionName)
                                t_file.write(f.read())
                        except Exception as e:
                            print(str(e)+'>>>>'+doc)
        if not writeFlag:
            for doc in file_list:
                arr.append(doc)
                print('----------' + doc)
                if '答案' in doc:
                    try:
                        with open('*'+file+'(答案).doc','a') as t_file,open(doc) as f:
                            sectionName = doc.replace('【答案】', '-').replace('.doc', '\n')
                            if sectionName[0]=='-':
                                sectionName=sectionName[1:]
                            t_file.write(sectionName)
                            t_file.write(f.read())
                    except Exception as e:
                        print(str(e) + '>>>>' + doc)
                else:
                    try:
                        with open('*'+file+'.doc', 'a') as t_file, open(doc) as f:
                            sectionName = doc.replace('.doc', '\n')
                            t_file.write(sectionName)
                            t_file.write(f.read())
                    except Exception as e:
                        print(str(e)+'>>>>'+doc)
        # print(arr)
        temp=[a for a in file_list if a not in arr]
        print(file+'--')
        print(temp)
        os.chdir('..')
# spider=Spider()
# spider.prepare_sections()
# spider.main()
# spider.multi_process()
reorganize_to_one_file()