# -*- encoding:utf8 -*-
from PyQt4.QtGui import QTabWidget,QStandardItemModel
from PyQt4.QtCore import QFileInfo
from heStruct.heSignal import connect,fire
from heQt.code_editor import CodeEditor
from lexer_completer.lexer_python import LexerPython
import chardet

class EditorManager(QTabWidget):
    def __init__(self, parent=None):
        super(EditorManager,self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.removeTab)
        connect('open_file',self.open_file)
        self.currentChanged.connect(self.on_switch_win)
    
    def on_switch_win(self,index):
        if hasattr(self.currentWidget(),'model'):
            fire('outline_set_model',self.currentWidget().model)   #[2] 在[1]处添加了model属性。
        else:
            fire('outline_set_model',QStandardItemModel())
        fire('code_encoding',self.currentWidget().encoding)
    
    def save_current_content(self):    
        win=self.currentWidget()
        #with open(win.path,'w') as f:
            #f.write(win.text().encode(win.encoding))
        print(win.text())
    
    def save_all_content(self):
        for win in self.get_wins():
            pass
    
    def open_file(self,path):
        win = self._check_if_opend(path)
        if win:
            self.setCurrentWidget(win)
        else:
            editor=CodeEditor(self)
            editor.model=QStandardItemModel()   #[1]注意，在这里为editor添加了model属性，便于在[2]使用。。
            #莫名多了该model属性，【Todo】 需要改进这个设计
            
            if path.endswith('.py'):
                editor.setLexer(LexerPython(editor,editor.model))            
            editor.path=path
            with open(path) as f:
                text=f.read()
                encoding=chardet.detect(text).get('encoding')
                if encoding!='utf-8':
                    text=text.decode(encoding)
                    text=text.encode('utf-8')
                editor.setText(text) 
                editor.encoding=encoding
                editor.emptyUndoBuff()
                editor.setSavePoint()
                editor.SAVEPOINTLEFT.connect(self.mark_editor_modifyed)
                editor.SAVEPOINTREACHED.connect(self.mark_editor_modifyed)
            fileinfo=QFileInfo(path)
            index=self.addTab(editor,fileinfo.fileName())
            self.setCurrentIndex(index)
            
    def mark_editor_modifyed(self): 
        win=self.sender()
        index = self.indexOf(win)
        if index !=-1:
            label_text=self.tabText(index)
            if win.isModified():
                label_text+='*'
            else:
                label_text=label_text.rstrip('*')
            self.setTabText(index,label_text)
        
    def _check_if_opend(self,path):
        for win in self.get_wins():
            if win.path==path:
                return win
            
    def get_wins(self):
        cnt=self.count()
        for i in range(cnt):
            yield self.widget(i)
    
    def save(self):
        return [win.path for win in self.get_wins()]
    
    def restore(self,dc):
        if dc is None:
            return
        for path in dc:
            self.open_file(path)
            
    def __reduce__(self):
        dc={'title':self.windowTitle()}
        return self.__class__,tuple(),dc
    
    def __setstate__(self,state):
        self.setWindowTitle(state['title'])