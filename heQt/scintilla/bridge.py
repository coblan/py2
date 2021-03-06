# -*- coding: utf-8 -*-
from PySide.QtCore import * 
from PySide.QtGui import *
from heStruct.pyeven import *
from ctypes import *
import sys,os
from heQt.scintilla.const import * 
# Mokia的约束
##os.environ['path']+=r';D:\develop\dlls'
##os.environ['path']+=r'd:\coblan\dlls'
os.environ["path"] += r";d:\coblan\dlls"
lib = CDLL("myScintilla.dll")
#lib = cdll.LoadLibrary('myScintilla.dll')

lib.newEditor.argtypes = [c_char_p]
lib.setEditorVar.argtypes = [c_char_p]


lib.textRange.restype = c_char_p
lib.text.restype = c_char_p
lib.textLine.restype = c_char_p


lib.send.argtypes = [c_long, c_long, c_long]
lib.send_i_c.argtypes = [c_int, c_long, c_char_p]
lib.send_c_c.argtypes = [c_int, c_char_p, c_char_p]
lib.send.restype = c_long
lib.send_i_c.restype = c_long
lib.send_c_c.restype = c_long

FUN_V_B = CFUNCTYPE(c_void_p, c_bool)

FUN_V_I_I = CFUNCTYPE(c_void_p, c_int, c_int)
FUN_B_I_I = CFUNCTYPE(c_bool, c_int, c_int)
MO_FUN = CFUNCTYPE(c_void_p, c_int, c_int, c_int, c_int, c_char_p, c_int, c_int, c_int)
FUN_V_I_I_I = CFUNCTYPE(c_void_p, c_int, c_int, c_int)

count = 0
def libInitEditor(obj):
    """赋予obj一个名字，在C++端生成一个editor对象，以obj的名字为线索，将editor依附于obj上"""
    global count
    count += 1
    obj.setObjectName("editor%s" % count)
    lib.newEditor(obj.objectName().encode("utf8"))
    
def librun(obj, funName, *args):
    """首先根据obj的名字，设置C++端的当前eidtor对象，再调用相应的函数"""
    lib.setEditorVar(obj.objectName().encode("utf8"))
    return getattr(lib, funName)( *args)
      

def u(text):
    return text.decode("utf8")
def b(ustr):
    return ustr.encode("utf8")

class Bridge(QWidget):
    """对象C++代码"""
    def __init__(self, parent=None):
        s( Bridge, parent)
        
        #在C++端生成一个sciEditor
        libInitEditor(self)
 
        self.__setCallback()
        
    def __setCallback(self):
        """设置C++端的回调函数"""
        self.__wn_modify = MO_FUN(self.onModify)
        self.__beforeKeyFun = FUN_B_I_I(self.beforeKey)
        self.__afterKeyFun = FUN_V_I_I(self.afterKey)
        self.__doubleClickFun = FUN_V_I_I(self.doubleClick)
        self.__mouseClickFun = FUN_V_I_I(self.mouseClick)
        self.__savePointChangedFun = FUN_V_B(self.savePointChanged)
        librun(self, "setCallback", self.__wn_modify , self.__beforeKeyFun, self.__afterKeyFun, self.__doubleClickFun, \
               self.__mouseClickFun, self.__savePointChangedFun)
    
    def beforeKey(self, key, modifier):
        "如果要消耗掉这个 keyPress，就返回True"
        return None
    def afterKey(self, key, modifier):
        pass
    def doubleClick(self, pos , line):
        pass
    def mouseClick(self, line, modifier):
        print(line, modifier)
    def savePointChanged(self, dirty):
        pass
    def onModify(self, type_, pos, length, linesAdd, text, line, foldNow, foldPre):
        "CALLBACK , 文档变化时 自动调用"
        print("Modify callback _has entered")  
    def setFormatList(self, c_range_array, comment_array):
        librun(self, "setFormatList", c_range_array, len(c_range_array), comment_array, len(comment_array))    
  
    def send(self, message, wPar = 0, lPar = 0):
        if isinstance(wPar, str):
            wPar = wPar.encode("utf8")
        if isinstance(lPar, str):
            lPar = lPar.encode("utf8")
            
        if isinstance(wPar, bytes):
            if isinstance(lPar, bytes):
                fun = "send_c_c"
        elif isinstance(lPar, bytes):
            fun = "send_i_c"
        else:
            fun = "send"
            
        return librun(self, fun, message, wPar, lPar)
    def text(self):
        return librun(self, "text")
       
    def textRange(self, start, end):
        return librun(self, "textRange", start, end)
    def textLine(self, line):
        return librun(self, "textLine", line)
   
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = Bridge()
    win.send(SCI_SETMARGINTYPEN, 1, 0)
    win.send(SCI_SETMARGINWIDTHN, 0, 40)
    win.show()
    #win.setToolTip("toooool tip")
    #for i in range(5):
        #win.setMarginWidthBit(i, 0)
    #win.addNumPanel(5)
    #win.setMarginTypeN(1, 0)
    #win.setMarginWidthBit(1, 1)
    #win.styleSetFore(33, QColor(Qt.blue))
    #win.styleSetBack(33, QColor(Qt.lightGray))
    sys.exit(app.exec_())