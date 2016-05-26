

class Tmp(object):
    def __init__(self):
        self.file=open(r'd:/try/fuck.meme','wb')
    
    def process_item(self, item, spider):
        self.file.write(str(item))
        return item