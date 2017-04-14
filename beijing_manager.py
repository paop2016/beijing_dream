import pymongo.mongo_client
import pymongo
class Manager():
    def __init__(self):
        self.db=pymongo.mongo_client.MongoClient('127.0.0.1',27017).beijing.ipmph
        while True:
            a=self.db.update({'status':'0'},{'$set':{'status':'1'}})
            if not a['updatedExisting']:
                break
    def save_sections(self,sections_ifo):
        self.db.remove()
        for section_ifo in sections_ifo:
            self.db.insert({'_id':section_ifo[1],'chapter_name':section_ifo[0],'section_name':section_ifo[2],'status':'1'})
    def get_one_sectionDic(self):
        return self.db.find_and_modify(query={'status':'1'},update={'$set':{'status':'0'}})