from PyQt4.QtCore import QObject,pyqtSlot,pyqtSignal
from difflib import ndiff,HtmlDiff
import json
import os


class Dog(QObject):
    def __init__(self, parent=None):
        super(Dog,self).__init__()
        self.files=[]
    
    @pyqtSlot(result=str)
    def get_files(self):
        return json.dumps(self.files)
    
    @pyqtSlot(str,str,result=str)
    def diff_file(self,src,dst):
        if os.path.exists(src) and os.path.exists(dst):
            with open(src) as f:
                aa = f.readlines()
            
            with open(dst) as f:
                bb = f.readlines()   
            
            print(HtmlDiff().make_file(aa,bb))
            return HtmlDiff().make_file(aa,bb)
        else:
            return 'some file not exist'
        
    @pyqtSlot(result=str)
    def content(self):
        print(self.frame.toHtml())
        return self.frame.toHtml()