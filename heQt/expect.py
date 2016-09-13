import qteven
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os


class Expect(QObject):
    def __init__(self, parent=None):
        super(Expect,self).__init__(parent)
        
        self.task = []
        self.proc =None
        self.update_proc()

    
    def update_proc(self):
        #if self.proc:
            #self.proc.setParent(None)
        self.proc = QProcess(self)
        self.proc.readyReadStandardOutput.connect(self.stdout)
        self.proc.started.connect(self.stdout)
        self.proc.error.connect(self.stdout)
        self.proc.finished.connect(self.on_finish)
        self.proc.stateChanged.connect(self.fetch_task)
        self.proc.started.connect(self.on_start)        
        
    def run(self,string):
        self.task.append(string)
        self.fetch_task()
    
    def fetch_task(self):
        state = self.proc.state()
        if state == QProcess.NotRunning and self.task:
            string = self.task.pop()
            #self.update_proc()
            self.proc.start(string)
        
    def stdout(self):
        string = self.proc.readAllStandardOutput().data()
        print(string )
        if string == 'show me':
            self.proc.write('heyulin\n')
        if string.find("Username for 'https://git.oschina.net'")!=-1:
            self.proc.write('coblan@163.com\n')
        if string.find("Password for 'https://coblan@163.com@git.oschina.net'")!=-1:
            self.proc.write('he7125158')
    
    def on_finish(self):
        print('finished ...')
    
    def on_start(self):
        print('started ...')

if __name__ == '__main__':
    app =QApplication(sys.argv)
    exp = Expect()
    
    os.chdir(r'D:\coblan\py2\heTools')
    #os.chdir(r'D:\coblan\py2\try')
    #exp.run(u'cmd /k dir')
   
    #exp.proc.start('cmd /c dir')
    exp.proc.start('fab push')
    #exp.proc.start('fab tt')
    #exp.run(u'python fabfile.py')
    sys.exit(app.exec_())