from beijing_manager import Manager
from beijing_downloader import Downloader
from beijing_parser import Parser
from beijing_outputer import Outputter
from urllib import request,parse
import urllib
class Spider():
    def __init__(self):
        self.manager=Manager()
        self.downloader=Downloader()
        self.parser=Parser()
        self.outputter=Outputter()


    def handleSection(self):
        pass
    def main(self):
        pass
spider=Spider()

