# -*= encoding:utf8 -*-
from heQt.qteven import *
from PyQt4.QtGui import QApplication,QStandardItemModel,QStandardItem,QColor
from PyQt4.QtCore import QByteArray
from PyQt4.Qsci import QsciScintilla,QsciLexerHTML,QsciLexer
import const

from autocompleter import Autocompleter,AutoModel
class Bridge(QsciScintilla):
    def __init__(self, parent=None):
        super(Bridge,self).__init__(parent)
        
        lexer = QsciLexerHTML(self)
        lexer.setColor(QColor('green'),style=QsciLexerHTML.Tag)
        #self.setLexer(const.SCLEX_NULL)
        self.setLexer(lexer)
        self.lexer= None #CusLexer(self)
        self._autoCompleter=None
        self.SCN_MODIFIED.connect(self.onModify)
    def setLexer(self,lexer):
        if isinstance(lexer,QsciLexer):
            super(Bridge,self).setLexer(lexer)
        else:
            self.lexer = lexer
        
    def send(self,*args,**kw):
        return self.SendScintilla(*args,**kw)
        
    def onModify(self, pos,type_,text,length,lineAdded,line,foldLevelNow,foldLeverPre,token,annot):
        """
        标准的scintiall这个回调函数的参数是：
        type_, pos, length, linesAdd, text, line, foldNow, foldPre
        但是pyqt封装之后的参数是：
         emit qsb->SCN_MODIFIED(scn.position, scn.modificationType, text,
                    scn.length, scn.linesAdded, scn.line, scn.foldLevelNow,
                    scn.foldLevelPrev, scn.token, scn.annotationLinesAdded);
        """
        
        if type_ & const.SC_MOD_BEFOREDELETE:
            # 删除前，暂时无用
            pass
            #self.contentChanged('beforeDel', pos, length)
        elif type_ & const.SC_MOD_BEFOREINSERT:
            # 插入前，暂时无用
            pass
    
            #self.contentChanged('beforeInsert', pos, length)
            
        elif type_ & const.SC_MOD_INSERTTEXT:
            if self.lexer:
                self.lexer.insertEvent(pos, length)

        elif type_ & const.SC_MOD_DELETETEXT:
            if self.lexer:
                self.lexer.deleteEvent(pos,length)
            #self.contentChanged('delete', pos, length) 
        
    def keyPressEvent(self,QKeyEvent):
        if self._autoCompleter:
            self._autoCompleter.beforeKey(QKeyEvent.key(),QKeyEvent.modifiers())               
        rt = super(Bridge,self).keyPressEvent(QKeyEvent)
        if self._autoCompleter:
            self._autoCompleter.afterKey(QKeyEvent.key(),QKeyEvent.modifiers()) 
        
        return rt
              
    def textRange(self,start, end):
        byt = bytearray(end-start)
        self.send(const.SCI_GETTEXTRANGE,start,end,byt)
        return str(byt)
    def currentPos(self):
        return self.send(const.SCI_GETCURRENTPOS)    
    def lineFromPos(self, pos):
        return self.send(const.SCI_LINEFROMPOSITION, pos)
    def posFromLine(self, line):
        return self.send(const.SCI_POSITIONFROMLINE, line)
    def lineLen(self, line):
        return self.send(const.SCI_LINELENGTH, line) 
    def getTextLength(self):
        return self.send(const.SCI_GETTEXTLENGTH) 
    def getStyleAt(self, pos):
        """返回某pos处的style number"""
        return self.send(const.SCI_GETSTYLEAT, pos)   
    def setAutoCompleter(self, comp):
        self._autoCompleter = comp    
    def pointXFromPos(self, pos):
        return self.send(const.SCI_POINTXFROMPOSITION, 0, pos)
    def pointYFromPos(self, pos):
        return self.send(const.SCI_POINTYFROMPOSITION, 0, pos)  
    def lineHeight(self):
        """所有行都是一样高的"""
        return self.send(const.SCI_TEXTHEIGHT, 0)  
    def replaceRange(self, text, pos, len_):
        """@text : utf8"""
        self.send(const.SCI_BEGINUNDOACTION)
        self.send(const.SCI_DELETERANGE, pos, len_)
        self.insertText(pos, text)
        self.send(const.SCI_ENDUNDOACTION)  
    def insertText(self, pos, text):
        if isinstance(text,unicode):
            text=text.encode('utf8')
        self.send(const.SCI_INSERTTEXT, pos, text)   
    def gotoPos(self, pos):
        self.send(const.SCI_GOTOPOS, pos)    

def test_adapte():
    from adaptLexer import AdaptLexer,Hello
    window.setLexer(Hello(window))
    auto = Autocompleter(window)
    window.setAutoCompleter(auto)
    model = QStandardItemModel()
    model.appendRow(QStandardItem('hello'))
    automodel=AutoModel()
    automodel._primModel = model
    auto.setAutoModel(automodel)    
def test_cuslexer():
    from cusLexer import CusLexer,Hello
    window.setLexer(Hello(window))
    auto = Autocompleter(window)
    window.setAutoCompleter(auto)
    model = QStandardItemModel()
    model.appendRow(QStandardItem('hello'))
    automodel=AutoModel()
    automodel._primModel = model
    auto.setAutoModel(automodel)    
if __name__ =='__main__':
    import sys
    app = QApplication(sys.argv)
    window = Bridge()
    test_cuslexer()
    #test_adapte()
    window.show()
    app.exec_()