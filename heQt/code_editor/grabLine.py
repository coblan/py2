# -*- encoding:utf8 -*-

class GrabLineManager(object):
    def __init__(self,editor):
        self.editor=editor
        self.grabedLines = []
    def grabLine(self, line):
        """抓住第line行"""
        wrap = GrabLine(line, self)
        self.grabedLines.append(wrap)
        return wrap
    
    def lineAddedEvent(self, pos, lineAdd):
        """CALLBACK ,当行数发生变化时，利用该函数调整以前抓住的行"""
        line = self.editor.lineFromPos(pos)
        if lineAdd > 0:
            for itm in self.grabedLines:
                #item_line = itm.line
                item_line=itm.lineNum()
                if item_line > line:
                    #itm.line = item_line + lineAdd 
                    itm.set_lineNum(item_line + lineAdd )
        elif lineAdd < 0:
            ls = []
            for itm in self.grabedLines:
                item_line=itm.lineNum()
                if line < item_line <= line + abs(lineAdd):
                    ls.append(itm)
                #elif line < num:
                elif line + abs(lineAdd)<item_line:
                    #itm.line = item_line - abs(lineAdd)
                    itm.set_lineNum(item_line - abs(lineAdd))
   
            for itm in ls:
                itm.del_handler()
                self.grabedLines.remove(itm) 
                
class GrabLine(object):
    "抓行对象//self.afterLineDel()  # CALLBACK 行被删除的时候调用"
    def __init__(self, line, editor):
        self.line = line
        self.editor = editor
        self.on_del = None
        self.onChanged=None
        
    def set_callback(self,onDel=None,onChanged=None):
        if onDel:
            self.on_del=onDel
        if onChanged:
            self.onChanged=onChanged
            
    def set_lineNum(self,line_num):
        self.line=line_num
        if self.onChanged:
            self.onChanged(line_num)
        
    def lineNum(self):
        return self.line
    
    def del_handler(self):
        if self.on_del:
            self.on_del()  # CALLBACK 行被删除的时候调用
        #self.uninstall()
        
    #def uninstall(self):         # 当不追踪该行时，记得调用该函数
        #if self in self.editor.grabedLines:
            #self.editor.grabedLines.remove(self)
    def __eq__(self, other):
        return self is other    