# -*- encoding:utf8 -*-

import sys,os

sys.path.append("python")
os.environ["path"] += ";dlls"

from PySide.QtGui import *
from PySide.QtCore import *
from selwin_ui import Ui_Form
from record import Record
import json

class ManulWin(QWidget,Ui_Form):
    def __init__(self,parent=None):
        super(ManulWin,self).__init__(parent)
        self.setupUi(self)
        
        self.record =None
        self.text_explain.setText(u"""
        这里是说明
        说明第一行
        """)
        self.btn_src.clicked.connect(self.sel_src)
        self.btn_dst.clicked.connect(self.sel_dst)
        self.btn_preprocess.clicked.connect(self.pre_process)
        self.btn_process.clicked.connect(self.process)
    
    def sel_src(self):
        name,filter_ = QFileDialog.getOpenFileName(filter="Excel03 (*.xls)")
        self.text_src.setText(name)
    
    def sel_dst(self):
        name,filter_ = QFileDialog.getSaveFileName(filter="Excel07 (*.xlsx)")
        self.text_dst.setText(name)
        
    def pre_process(self):
        src = self.text_src.text()
        dst = self.text_dst.text()
        self.record = Record(src, dst)
        info = self.record.pre_process()
        workday=[]
        restday=[]
        for d in info:
            if d.weekday()==5 or d.weekday()==6:
                restday.append(d)
            else:
                workday.append(d)
        workday = [x.strftime("%Y/%m/%d") for x in workday]
        restday = [x.strftime("%Y/%m/%d") for x in restday]
        dc = {"time":{"workday":("8:30","17:30"),
                      "special":("10:00","17:30")
                      },
              "workday":workday,
              "restday":restday,
              "special":[]} 
        self.text_manul.setPlainText(json.dumps(dc,indent=4))
            
        
    def process(self):
        daysettings= self.text_manul.toPlainText()
        daysettings= json.loads(daysettings)
        self.record.process(daysettings,self.text_dst.text())
        QMessageBox.information(None,u"通知",u"处理完成")

if __name__=='__main__':
    app =QApplication(sys.argv)
    win = ManulWin()
    win.show()
    sys.exit(app.exec_())