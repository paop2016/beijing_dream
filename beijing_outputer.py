import os
class Outputter():
    def __init__(self,file):
        try:
            os.mkdir(file)
        except FileExistsError:
            if file[-1]=='程':
                new_file=file+'1'
            else:
                index = file.index('程')
                new_file = file[:index+1]+str(int(file[index+1:])+1)
            self.__init__(new_file)
            return
        else:
            print('正创建文件夹>>>%s' % file)
        os.chdir(file)
    def write_file(self,section,content):
        self.createFile(section['chapter_name'])
        try:
            with open(self.get_txt_name(section['chapter_name'],section['section_name']),'w') as f:
                f.write(content[0])
            with open(self.get_txt_name(section['chapter_name'],section['section_name'],True),'w') as f:
                f.write(content[1])
        except Exception as e :
            print('写文件出错>>'+str(e))

    def createFile(self,chapter_name):
        try:
            os.mkdir(chapter_name)
        except FileExistsError:
            pass

    def get_txt_name(self,chapter_name,section_name,answer_flag=False):
        section_name=section_name.replace('章 ','节 ')
        index = section_name.find('节')
        if answer_flag:
            if index==-1:
                return chapter_name + '/【答案】' + section_name + '.doc'
            else:
                return chapter_name + '/' + section_name[:index+1]+'【答案】'+section_name[index+2:] + '.doc'
        else:
            if index==-1:
                return chapter_name + '/' + section_name + '.doc'
            else:
                return chapter_name+'/'+section_name[:index+1]+'-'+section_name[index+2:]+'.doc'