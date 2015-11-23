# -*- encoding:utf8 -*-

import sys,os

sys.path.append("python")
os.environ["path"] += ";dlls"

from PySide.QtGui import *
from PySide.QtCore import *
from selwin_ui import Ui_Form
from record import pre_process,process
import json

class ManulWin(QWidget,Ui_Form):
    def __init__(self,parent=None):
        super(ManulWin,self).__init__(parent)
        self.setupUi(self)
        
        self.record =None
        self.text_explain.setText(u"""
    设置日期，哪些是工作日，哪些不工作，以及工作日的作息时间等。
    格式如下: 虚线之间
---------------------------------------------
    {
    "workday": [
        "2015/09/01", 
        "2015/09/02", 
        ...
    ], 
    "restday": [
        "2015/09/05", 
        "2015/09/06", 
        ...
    ], 
    "special": [], 
    "time": {
        "special": [
            "10:00", 
            "17:30"
        ]
    }
}
---------------------------------------------------
    其中：
    workday 按照个人workshift计算上班下班时间
    restday 不计算个人迟到早退
    special  按照time中设置的时间计算上下班
    中午午饭:12:30-1:30不计算在工作时长中。
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
        #dst = self.text_dst.text()
        #self.record = Record(src, dst)
        #info = self.record.pre_process()
        days = pre_process(src)
        workday=[]
        restday=[]
        for d in days:
            if d.weekday()==5 or d.weekday()==6:
                restday.append(d)
            else:
                workday.append(d)
        workday = [x.strftime("%Y/%m/%d") for x in workday]
        restday = [x.strftime("%Y/%m/%d") for x in restday]
        dc = {"time":{"special":("10:00","17:30")
                      },
              "workday":workday,
              "restday":restday,
              "special":[]} 
        self.text_manul.setPlainText(json.dumps(dc,indent=4))
            
        
    def process(self):
        dst = self.text_dst.text()
        daysettings= self.text_manul.toPlainText()
        daysettings= json.loads(daysettings)
        process(daysettings, dst)
        #self.record.process(daysettings,self.text_dst.text())
        QMessageBox.information(None,u"通知",u"处理完成")

if __name__=='__main__':
    app =QApplication(sys.argv)
    win = ManulWin()
    win.show()
    sys.exit(app.exec_())