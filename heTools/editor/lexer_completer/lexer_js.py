# -*- encoding:utf8 -*-

import sys
from heQt.code_editor import CusLexer
from PyQt4.QtGui import QColor,QFont,QStandardItemModel,QStandardItem
from PyQt4.QtCore import Qt
import re
from heStruct.heSignal import connect

class LexerJs(CusLexer):
    def __init__(self, editor,model):
        super(LexerJs,self).__init__(editor)
        self.outline=OutlineProc(editor,model)
        self.setForeColor(18,QColor('blue'))
        self.setForeColor(1,QColor('green'))

        font2=QFont()
        font2.setFamily('Courier New')
        font2.setPointSize(10)
        self.setStyleFont(32,font2)
        self.setForeColor(32,QColor('black'))
        
        font=QFont(font2)
        font.setBold(True)
        font.setItalic(True)
        self.setStyleFont(18,font)        
        
    def hightText(self, start, end):
        self.setFormat(start, end, 32)
        text = self.editor.textRange(start, end)
        for i in re.finditer('function|\$', text):
            self.setFormat( start+i.start(),start+i.end(),18)  
        for i in re.finditer('//.*?$',text,re.MULTILINE):
            self.setFormat( start+i.start(),start+i.end(),1)  
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
        self.del_outdate_gb(start, text)
        self.add_outline_item(start, text)
    
    def del_outdate_gb(self,start,text):
        if not re.match(r'^//\[(.*?)\]',text):
            line_num=self.editor.lineFromPos(start)
            if line_num in [gb.line for gb in self.grab_lines]:
                index=[gb.line for gb in self.grab_lines].index(line_num)
                if index!=-1 :
                    gb=self.grab_lines[index]
                    self.remove_grab_line(gb)
    
    def add_outline_item(self,start,text):
        for i in re.finditer(r'^//\[(.*?)\]',text,re.MULTILINE):
            pos=start+i.start()
            line_num=self.editor.lineFromPos(pos)
            if line_num not in [gb.line for gb in self.grab_lines] :
                gb=self.editor.grabLine(line_num)
                self.grab_lines.append(gb)
                item=QStandardItem(i.group(1).decode('utf8'))
                item.setData(line_num,Qt.UserRole+1)
                #gb.item.gb=gb
                gb.item=item         #[1] 这里给grabline对象，加了个item属性，是为了[2]中更新大纲的文字
                def ondel():
                    self.remove_grab_line(gb)
                def onchanged(num):
                    item.setData(num,Qt.UserRole+1)
                gb.set_callback(onDel=ondel,onChanged=onchanged)
                self.model.appendRow(item)
                self.model.sort(0)
            else:
                index=[gb.line for gb in self.grab_lines].index(line_num)
                self.grab_lines[index].item.setData(i.group(1).decode('utf8'),Qt.DisplayRole)     # [2]            
    def remove_grab_line(self,gb):
        item=gb.item
        self.model.removeRow(item.row())
        self.grab_lines.remove(gb)        
            
    