# -*- encoding:utf8 -*-

from heQt.code_editor import CusLexer
from PyQt4.QtGui import QColor,QFont,QStandardItemModel,QStandardItem
from PyQt4.QtCore import Qt
import re
from heStruct.heSignal import connect
#if 0:
    #from heQt.code_editor import CodeEditor
class LexerPython(CusLexer):
    def __init__(self, editor,model):
        super(LexerPython,self).__init__(editor)
        self.outline=OutlineProc(editor,model)
        
        self.setForeColor(18,QColor('blue'))
        self.setForeColor(1,QColor('green'))
        font=QFont()
        font.setBold(True)
        font.setItalic(True)
        self.setStyleFont(18,font)
        self.setForeColor(32,QColor('black'))
           
    def hightText(self, start, end):
        self.setFormat(start, end, 32)
        text = self.editor.textRange(start, end)
        for i in re.finditer('class|def', text):
            self.setFormat( start+i.start(),start+i.end(),18)  
        for i in re.finditer('#.*?$',text,re.MULTILINE):
            self.setFormat( start+i.start(),start+i.end(),1)  
        #self._update_outline(start, text)
        self.outline.update_outline_model(start, text)
        

                
class OutlineProc(object):
    def __init__(self,editor,model):
        self.editor=editor
        self.model=model
        self.model.setSortRole(Qt.UserRole+1)        
        self.grab_lines=[]
    
        connect('outline_click_item',self.on_outline_click_item)
    def on_outline_click_item(self,model,item):
        if model!=self.model:
            return
        else:
            #self.editor.scrollToLine(item.gb.line )
            pos=self.editor.posFromLine(item.data(Qt.UserRole+1))
            pos+= len( item.data(Qt.DisplayRole).encode('utf8') ) 
            self.editor.gotoPos(pos)
            self.editor.setFocus(True)        
    
    def update_outline_model(self,start,text):
        for i in re.finditer('^#!(.*?)$',text,re.MULTILINE):
            pos=start+i.start()
            line_num=self.editor.lineFromPos(pos)
            if line_num not in [gb.line for gb in self.grab_lines] :
                gb=self.editor.grabLine(line_num)
                self.grab_lines.append(gb)
                item=QStandardItem(i.group(1).decode('utf8'))
                item.setData(line_num,Qt.UserRole+1)
                #gb.item.gb=gb
                gb.item=item         #[1] 这里给grabline对象，加了个item属性，是为了[2]中更新大纲的文字
                def fuck():
                    print('fuck')
                def onchanged(num):
                    item.setData(num,Qt.UserRole+1)
                gb.set_callback(onDel=fuck,onChanged=onchanged)
                self.model.appendRow(item)
                self.model.sort(0)
            else:
                index=[gb.line for gb in self.grab_lines].index(line_num)
                self.grab_lines[index].item.setData(i.group(1).decode('utf8'),Qt.DisplayRole)     # [2]        
    