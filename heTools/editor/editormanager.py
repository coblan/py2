# -*- encoding:utf8 -*-
from PyQt4.QtGui import QTabWidget,QStandardItemModel
from PyQt4.QtCore import QFileInfo,pyqtSignal
from heStruct.heSignal import connect,fire
from heQt.code_editor import CodeEditor
from lexer_completer.lexer_python import LexerPython
from lexer_completer.lexer_js import LexerJs
import chardet

class EditorManager(QTabWidget):
    undoStateChanged=pyqtSignal(bool,bool)
    currentEncodeChanged=pyqtSignal(str)
    def __init__(self, parent=None):
        super(EditorManager,self).__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.removeTab)
        connect('open_file',self.open_file)
        self.currentChanged.connect(self.on_switch_win)
    
    def undo(self):
        win=self.currentWidget()
        if win.canUndo():
            win.undo()
            
    def redo(self):
        win=self.currentWidget()
        if win.canRedo():
            win.redo()

    def on_switch_win(self,index):
        win=self.currentWidget()
        if hasattr(win,'model'):
            fire('outline_set_model',win.model)   #[2] 在[1]处添加了model属性。
        else:
            fire('outline_set_model',QStandardItemModel())
        if self.currentWidget():
            # fire('code_encoding',self.currentWidget().encoding)
            self.currentEncodeChanged.emit(win.encoding)
        self.undoStateChanged.emit(win.canUndo(),win.canRedo())
    
    def save_current_content(self):    
        win=self.currentWidget()
        text=win.text().decode('utf8')
        with open(win.path,'w') as f:
            f.write(text.encode(win.encoding))
            win.setSavePoint()
    
    def save_all_content(self):
        for win in self.get_wins():
            pass
    
    def open_file(self,path):
        win = self._check_if_opend(path)
        if win:
            self.setCurrentWidget(win)
        else:
            editor=win_factory(path)
            if editor:
                editor.SAVEPOINTLEFT.connect(self.mark_editor_modifyed)
                editor.SAVEPOINTREACHED.connect(self.mark_editor_modifyed)
                fileinfo=QFileInfo(path)
                index=self.addTab(editor,fileinfo.fileName())
                self.setCurrentIndex(index)
                editor.undoStateChanged.connect(self.undoStateChanged)
            
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
            
def win_factory(path):
    if path.endswith('.py'):
        editor=CodeEditor()
        editor.model=QStandardItemModel()          
        editor.setLexer(LexerPython(editor,editor.model)) 
    elif path.endswith('.js'):
        editor=CodeEditor()
        editor.model=QStandardItemModel()          
        editor.setLexer(LexerJs(editor,editor.model))         
    else:
        return
    editor.path=path
    text,encoding=open_rt_as_utf8_and_org_encoding(path)
    editor.setText(text) 
    editor.encoding=encoding
    editor.emptyUndoBuff()
    editor.setSavePoint()
    return editor

def open_rt_as_utf8_and_org_encoding(path):
    with open(path) as f:
        text=f.read()
        encoding=chardet.detect(text).get('encoding')
        if encoding!='utf-8':
            text=text.decode(encoding)
            text=text.encode('utf-8')  
    return text,encoding