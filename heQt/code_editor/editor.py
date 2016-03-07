# -*= encoding:utf8 -*-
from heQt.qteven import *
from heStruct.cls import sub_obj_call,add_sub_obj
from PyQt4.QtGui import QApplication,QStandardItemModel,QStandardItem,QColor
from PyQt4.QtCore import QByteArray,Qt
from PyQt4.Qsci import QsciScintilla,QsciLexerHTML,QsciLexer
import const
from grabLine import GrabLineManager

from autocompleter import Autocompleter,AutoModel
class CodeEditor(QsciScintilla):
    SAVEPOINTLEFT=pyqtSignal()
    SAVEPOINTREACHED=pyqtSignal()
    def __init__(self, parent=None):
        super(CodeEditor,self).__init__(parent)
        
        self.send(const.SCI_SETCODEPAGE, const.SC_CP_UTF8)
        
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#CDA869"))
        #lexer = QsciLexerHTML(self)
        #lexer.setColor(QColor('green'),style=QsciLexerHTML.Tag)
        ##self.setLexer(const.SCLEX_NULL)
        #self.setLexer(lexer)
        self.setMarginTypeN(0,const.SC_MARGIN_NUMBER)
        self.setMarginWidthN(0,40)
        
        self.lexer= None #CusLexer(self)
        self._autoCompleter=None
        self.grabline_manager=GrabLineManager(self)
        add_sub_obj(self,self.grabline_manager)
        
        self.SCN_MODIFIED.connect(self.onModify)
        self.SCN_SAVEPOINTLEFT.connect(self.SAVEPOINTLEFT)
        self.SCN_SAVEPOINTREACHED.connect(self.SAVEPOINTREACHED)
        self.setAttribute(Qt.WA_DeleteOnClose)
    
    def emptyUndoBuff(self):
        self.send(const.SCI_EMPTYUNDOBUFFER)
    
    def isModified(self):
        return False if self.send(const.SCI_GETMODIFY)==0 else True
    
    def setSavePoint(self):
        self.send(const.SCI_SETSAVEPOINT)
    
    def grabLine(self,line_num):
        """
        """
        return self.grabline_manager.grabLine(line_num)
    
    def lineFromPos(self,pos):
        return self.send(const.SCI_LINEFROMPOSITION,pos)
    
    def scrollToLine(self, line):
        "滚动显示到某行"
        self.setFirstVisibleLine( self.visibleFromDocLine( line ))
        
    def setFirstVisibleLine(self, line):
        self.send(const.SCI_SETFIRSTVISIBLELINE,line)
        
    def visibleFromDocLine(self,line):
        return self.send(const.SCI_VISIBLEFROMDOCLINE,line)
    
    def setLexer(self,lexer):
        if isinstance(lexer,QsciLexer):
            super(CodeEditor,self).setLexer(lexer)
        else:
            self.lexer = lexer
            add_sub_obj(self,self.lexer)
        
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
        if lineAdded!=0:
            self.lineAddedEvent(pos, lineAdded)
            
        if type_ & const.SC_MOD_BEFOREDELETE:
            # 删除前，暂时无用
            self.preDeleteEvent(pos, length)
            #self.contentChanged('beforeDel', pos, length)
        elif type_ & const.SC_MOD_BEFOREINSERT:
            # 插入前，暂时无用
            self.preInsertEvent(pos, length)
    
            #self.contentChanged('beforeInsert', pos, length)
            
        elif type_ & const.SC_MOD_INSERTTEXT:
            self.insertEvent(pos, length)
            #if self.lexer:
                #self.lexer.insertEvent(pos, length)

        elif type_ & const.SC_MOD_DELETETEXT:
            self.deleteEvent(pos, length)
            #if self.lexer:
                #self.lexer.deleteEvent(pos,length)
            #self.contentChanged('delete', pos, length) 

            
    def setText(self, text):
        self.send(const.SCI_SETTEXT, 0, text)    
    
    @sub_obj_call
    def lineAddedEvent(self,pos,lineAdded):
        pass
    
    @sub_obj_call
    def preInsertEvent(self,pos,length):
        pass
    
    @sub_obj_call
    def insertEvent(self,pos,length):
        pass
    
    @sub_obj_call
    def preDeleteEvent(self,pos,length):
        pass
    
    @sub_obj_call
    def deleteEvent(self,pos,length):
        pass
    
    def keyPressEvent(self,QKeyEvent):
        if self._autoCompleter:
            self._autoCompleter.beforeKey(QKeyEvent.key(),QKeyEvent.modifiers())               
        rt = super(CodeEditor,self).keyPressEvent(QKeyEvent)
        if self._autoCompleter:
            self._autoCompleter.afterKey(QKeyEvent.key(),QKeyEvent.modifiers()) 
        return rt
              
    def textRange(self,start, end):
        byt = bytearray(end-start)
        self.send(const.SCI_GETTEXTRANGE,start,end,byt)
        return str(byt)
    def text(self):
        length=self.send(const.SCI_GETLENGTH)
        byt = bytearray(length+1)
        self.send(const.SCI_GETTEXT,length+1,byt)
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
        
    def setMarginTypeN(self,margin,type_):
        self.send(const.SCI_SETMARGINTYPEN,margin,type_)
    
    def setMarginWidthN(self,margin,width):
        self.send(const.SCI_SETMARGINWIDTHN,margin,width)
        
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
    
def test_cuslexer(window):
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
    window = CodeEditor()
    test_cuslexer(window)
    #test_adapte()
    window.show()
    app.exec_()