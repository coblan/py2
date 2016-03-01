# -*- encoding:utf8 -*-
from PyQt4.QtCore import QObject
from PyQt4.QtGui import QColor
import re
import sys
from PyQt4.Qsci import QsciStyle
import const
if 0:
    from bridge import CodeEditor
    
def QcolorToRGB(color):
    r = color.red()
    g = color.green()
    b = color.blue()
    return (r | g << 8 | b << 16)

class CusLexer(QObject):
    """Lexer基类，构造函数直接 将lexer插在editor上
    
    重载 hightText 函数
    """     
    def __init__(self, editor):
        """可以在构造函数中设置各种样式。最好从1开始。
        self.editor.setForeColor(1,QColor('red'))
        """
        super(CusLexer,self).__init__(editor)
        self.editor = editor
        if 0: 
            assert isinstance(editor, CodeEditor)    
    

    def hightText(self, start, end):
        """在子类中，这里面写功能函数
        样例：
        text = self.editor.textRange(start, end)
        self.editor.setFormat(start, end, 32)
        
        match = dosome_math(text,pattern)
        ls=[(start + match.start(), start + match.end()，k)]   # k是style号

        self.editor.setFormatList(ls)
        """
        pass
    
    def insertEvent(self, pos, length):
        """总的促发高亮的 回调函数
        判断一下是否是最后一行，如果不是，还要单独刷新一下最后一行
        """
        self.hightRange(pos, length)
    
    def deleteEvent(self,pos, length):
        line = self.editor.lineFromPos(pos)
        self.hightLine(line)
        
    def hightRange(self, pos, length):
        line = self.editor.lineFromPos(pos)
        start = self.editor.posFromLine( line )
        endLine = self.editor.lineFromPos(pos + length)
        end = self.editor.posFromLine(endLine) + self.editor.lineLen(endLine) 
        
        self.hightText(start, end)
        
        # 由于最后一个字符高亮问题，所以每次都重新刷新一下最后一行
        self.bugLastWord()

    def hightLine(self, line):
        pos = self.editor.posFromLine(line)
        length = self.editor.lineLen(line)
        self.hightRange(pos, length)
           

    def bugLastWord(self):
        end = self.editor.getTextLength() - 1
        number = self.editor.getStyleAt(end)

        self.setFormat(end, end + 1, number)
    
    def setForeColor(self,n,color):
        #color = QcolorToRGB(QColor)
        self.editor.send(const.SCI_STYLESETFORE, n, color)
    def send(self,*args,**kw):
        return self.editor.SendScintilla(*args,**kw)
    def setFormat(self, start, end, n):
        self.send(const.SCI_STARTSTYLING, start)
        self.send(const.SCI_SETSTYLING, end - start, n)         

class Hello(CusLexer):
    def __init__(self, editor):
        super(Hello,self).__init__(editor)

        self.setForeColor(18,QColor('red'))
        self.setForeColor(32,QColor('blue'))
    
    
    def hightText(self, start, end):
        self.setFormat(start, end, 32)
        text = self.editor.textRange(start, end)
        for i in re.finditer('hello|fuck', text):
            self.setFormat( start+i.start(),start+i.end(),18)