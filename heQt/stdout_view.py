# -*- encoding:utf8 -*-
from qteven import *
import sys,re
from PyQt4.QtGui import QTextBrowser,QApplication,QSyntaxHighlighter,QTextCursor
from PyQt4.QtCore import QObject

class StdoutView(QTextBrowser):
    """例子
    快捷的设置sys.stdout对象
    win=StdoutView()
    sys.stdout=win.get_stdout_obj()
    sys.stderr = sys.stdout
    
    设置定时探针
    win.openSensor(5)  /win.openSensor_thd(5)
    do()
    win.sensor=“要显示的内容"
    do()
    win.closeSensor()  /win.closeSensor_thd()
    """
    openSensor_thd = Signal(int)
    closeSensor_thd = Signal()
    def __init__(self,*args):
        super(StdoutView,self).__init__(*args)
        self.sensor = "StdoutView default sensor"
        self.openSensor_thd.connect(self.openSensor)   # 但在非创建线程开启定时探测是，因为timer不能在 
        self.closeSensor_thd.connect(self.closeSensor)  # 非创建线程 启动，所以要利用signal来启动timer
        #self._has_msg = False
        #self._msg_cnt = 0
    def setAdaptor(self,adapt):
        if hasattr(self,'adaptor'):
            self.adaptor.cout.disconnect()
        self.adaptor=adapt
        self.adaptor.cout.connect(self.recieve)
        
    def recieve(self,arg):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.setTextCursor(cursor)
        self.insertPlainText(arg)
        bar=self.verticalScrollBar()
        bar.setSliderPosition(bar.maximum ())

    def get_stdout_obj(self):
        "快捷的方式，返回一个stdoutAdaptor对象。可以多次的调用，返回的都是同一个adapter"
        if hasattr(self, 'adaptor'):
            return self.adaptor
        else:
            self.setAdaptor(StdoutAdaptor())
        return self.adaptor
    def openSensor(self, sec):
        "开启传感器"
        sec = sec * 1000
        self.closeSensor()
        self._sensorTimer = self.startTimer(sec)
        
    def closeSensor(self):
        if hasattr(self, "_sensorTimer"):
            self.killTimer(self._sensorTimer)        
    def timerEvent(self, e):
        if hasattr(self, "_sensorTimer", ) and e.timerId() == self._sensorTimer:
            print self.sensor
    
class StdoutAdaptor(QObject):
    cout=pyqtSignal(unicode)
    def __init__(self,*args):
        super(StdoutAdaptor,self).__init__(*args)
    
    def write(self,arg):
        self.cout.emit(arg)    
        
class syntex(QSyntaxHighlighter):
    def __init__(self,*args):
        super(syntex,self).__init__(*args)
        self.keyword=re.compile('warning|ERROR|SEVERE',re.I)
    def highlightBlock(self,text):
        for ii in re.finditer(self.keyword,text):
            form=QTextCharFormat()
            form.setForeground(Qt.red)
            self.setFormat(ii.start(),ii.end()-ii.start(),form) 
        
if __name__=='__main__':
    app=QApplication(sys.argv)
    
    win=StdoutView()
    win.show()
    stdout=StdoutAdaptor()
    win.setAdaptor(stdout)
    
    sys.stdout=stdout
    
    print 'hello world'
    print 'fuck'
    sys.exit(app.exec_())