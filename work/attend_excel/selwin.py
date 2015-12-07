# -*- encoding:utf8 -*-

import sys,os

sys.path.append("python")
os.environ["path"] += ";dlls"

from PySide.QtGui import *
from PySide.QtCore import *
from selwin_ui import Ui_Form
from record2 import pre_process,process
import json

class ManulWin(QWidget,Ui_Form):
    def __init__(self,parent=None):
        super(ManulWin,self).__init__(parent)
        self.setupUi(self)
        
        self.record =None
        self.text_explain.setHtml(u"""
<pre>
当前实现的处理:
========================================================
1. 计算工作时长
2. 标记非工作日(restday)，漏打卡(single)，旷工(not work全天无打卡)
3. 计算加班时长，20：00后算加班.现在还不能调整加班计算时刻。
4. 根据非周末的加班，调整第二天上班时间到10：00。这里只针对非弹性工作制的员工，如果员工的workshfit规定上班时间迟于10：00，则不调整。
5. 计算早退时间。根据特殊工作作息 或 workshift来计算
6. 计算迟到等级 late1-late4
7. 计算团队迟到时间，根据迟到等级计算个人迟到时间

员工信息来源
======================================================
考勤记录中不包括个人的workshift信息，该信息本来应该来自于TMS，但是这里为了方便，暂时调用employee.xlsx文件的信息。
你可以在employee.xlsx中修改个人信息，然后再处理
</pre>

<div style="color:blue">使用步骤:</div>
<pre>
===============================================
1. 选择考勤记录的原始excel03文件
2. 选择准备输出的excel07文件名
3. 点击【预处理】,生成日期列表
4. 修改日期列表
5. 点击【处理】，处理，并生成excel07文件

日期列表设置
===============================================
   设置日期，哪些是工作日，哪些是非工作日，以及工作日的作息时间等。
   格式如下: 虚线之间，
</pre>
<span style="color:red">注意[]数组中的最后一项不能加逗号</span>
<pre>
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
        "10：00-17：50":[
           "2015/09/21",
           "2015/09/22"
        ] 
       }
      }
   ---------------------------------------------------
 * 其中：
    workday 正常工作日，按照个人workshift计算上班下班时间
    restday 非工作日，不计算个人迟到早退
    "10：00-17：50" 特殊作息工作日，按照10:00和17：50计算上下班时间
    
 * 中午午饭:12:30-1:30不计算在工作时长中。
    
</pre>
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
        dc = { "workday":workday,
              "restday":restday,
              "10:30-17:30":[]} 
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