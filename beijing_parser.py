from bs4 import BeautifulSoup
import re
class Parser():
    def __init__(self):
        pass
    def parse_chapters(self,resource):
        soup=BeautifulSoup(resource,'html.parser')
        chapters_ifo=[]
        for item in soup.find_all('div',class_=re.compile('list-group-item')):
            charter_name=item.contents[1].text.strip()
            chapter_id=re.search('\'\d+',item.contents[1].name).group()[1:]
            chapters_ifo.append([chapter_id,charter_name])
        return chapters_ifo
    def parse_sections(self,sections_html):
        sections_ifo=[]
        for section_html in sections_html:
            soup=BeautifulSoup(section_html[1],'html.parser')
            for item in soup.find_all('tr'):
                section_name=item.find_all('a', href=re.compile('/learncenter/'))[0].text.split('-')[-1]
                section_id=re.search("'\d+'",item.find_all('a',class_=re.compile('fco'))[0]['href']).group()[1:-1]
                sections_ifo.append([section_html[0],section_id,section_name])
        return sections_ifo
    def parse_section_detail(self,html):
        soup = BeautifulSoup(html, 'html.parser')
        content_no_answer = ''
        content_answer = ''
        for item in soup.find_all('div',class_='hide-some'):
            question=item.find('h2',class_='h4 m-b').text
            index1=question.index('.')
            index2=question.index('】')

            # A3A4题特殊处理 【大题题干】
            if '【A3/A4' in question:
                question_big=item.find('div',class_='PTitle').text[6:].strip()
                question_big='#'+question[:index1]+' '+question_big
                question = question[index1 + 1:index2 - 3].replace('/','') + question[index2:] + ':'
                content_no_answer=content_no_answer+question_big+'\n'
                content_answer=content_answer+question_big+'\n'
            else:
                question = '#' + question[:index1] + ' ' + question[index1 + 1:index2 - 3] + question[index2:] + ':'
            # 【问题】
            content_no_answer=content_no_answer+question+'\n'
            content_answer=content_answer+question+'\n'
            # 【选项】
            options=item.find_all('label',class_='i-checks')
            for option in options:
                option_text=option.text[:1]+'、'+option.text[2:]
                content_no_answer = content_no_answer + option_text + '\n'
                content_answer=content_answer+option_text+'\n'
            # 【答案】
            answer=item.find(class_='alert alert-warning',role='alert').text.strip()
            answer=answer.replace('【', '').replace('】', '')
            answers=answer.split('\n')
            content_answer=content_answer+'正确'+answers[0]+'\n'+answers[1].strip()+'\n'

            content_no_answer=content_no_answer+'\n'
            content_answer=content_answer+'\n'
        return [content_no_answer,content_answer]




