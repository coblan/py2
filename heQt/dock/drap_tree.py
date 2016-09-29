# -*- encoding:utf8 -*-
from heQt.qteven import *
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import pickle
import re
from heStruct.cls import add_sub_obj,sub_obj_call


class DockTab(QTabWidget):
    """
    
    默认增加功能：
    1 迭代窗口
    2 保存，恢复所有能够pickle的窗口
    
    重要函数：
    enableCrossDrag(Bar<-cls)           开启夸窗口拖拽功能
    enableChineseDirection(Bar<-cls)    开启中文调整方向功能
    
    注意：这两个函数的参数是Bar的子类，不是Bar的对象
  
    
    默认向QTabWidget增加的功能：
    1 迭代窗口a
    2 保存，恢复所有能够pickle的窗口
    
    可以开启功能：
    1 enableCrossDrag   自定义的拖动。可以垮Tabwidget拖动
    2 enableChineseDirection  中文旋转 。利用自绘中文来实现。
                              如果还需要拖动，最好开启"1 自定义拖动"，因为Qt自带拖动，自绘标签有空白。
    
    """
    def __init__(self, *args):
        super(DockTab,self).__init__( *args)
        self.enableCrossDrag()
        self.tabCloseRequested.connect(self.removeTab)

    def enableCrossDrag(self):
        """"""
        self.bar=BarBase(self)
        self.setTabBar(self.bar)
        self.crossDrag = TabWidget_crossDrag(self)
        self.crossDrag.drag_finish.connect(self.bar.comDrag.clear_line)
        self.crossDrag.drag_ing.connect(self.bar.comDrag.drawLine)
        add_sub_obj(self,self.crossDrag)
   
    @sub_obj_call
    def dragEnterEvent(self, event):
        pass
    
    @sub_obj_call
    def dropEvent(self, event):
        pass 
    
    @sub_obj_call
    def dragMoveEvent(self, event):
        super(DockTab,self).dragMoveEvent(event)
        
    @sub_obj_call
    def dragLeaveEvent(self, event):
        pass   
     
    def get_wins(self):
        crt_index=0
        while crt_index < self.count():
            yield self.widget( crt_index )
            crt_index += 1
                    

    #[2] 添加窗口，添加标签名，将名字标签名保存在windowTitle中
    def addTab(self, widget, name = ""):
        widget.setWindowTitle(name)
        if self.isNeedTurnDirection(name):
            return super(DockTab,self).addTab(widget, "")
        else:
            return super(DockTab,self).addTab(widget, name)
            
    def isNeedTurnDirection(self, text):
        if self.tabPosition() != QTabWidget.North:
            if re.search(u'[\u4e00-\u9fa5]+',text):
                return True
        return False   
    
    def insertTab(self, index, widget, name):
        widget.setWindowTitle(name)
        if self.isNeedTurnDirection(name):
            super(DockTab,self).insertTab(index, widget, "")
        else:
            super(DockTab,self).insertTab(index, widget, name)    
                
    def removeWidget(self, widget):
        index = self.indexOf(widget)
        if index >= 0:
            self.removeTab(index)
       
    #[3] 保存和恢复所有的窗口。保存数据是QByteArray形式，便于同qt对接
    def restoreWins(self, string):
        if not string:
            return
        if isinstance(string, QByteArray):
            string = string.data()
        dc = pickle.loads(string)
        ls = dc.get('wins', None)
        if ls:
            last = None
            currentWidget = None
            for ii in ls:
                if ii == "last is currentWidget":
                    currentWidget = last
                    continue
                else:
                    # 恢复窗口及其tabName属性
                    win, label, tip = pickle.loads(ii[0]), ii[1], ii[2]
                    index = self.addTab(win, label)
                    self.setTabToolTip(index, tip)
                    last = win
            if currentWidget:
                self.setCurrentWidget(currentWidget )
          

    
    def saveWins(self):
        ls = []
        index = -1
        for win in self.get_wins():
            index += 1
            try:
                winbyt = pickle.dumps(win)
                # 保存窗口及其tabName属性
                label = win.windowTitle()
                tip = self.tabToolTip(index)
                ls.append( (winbyt, label, tip) )
                if self.currentWidget() == win:
                    ls.append("last is currentWidget")          
            except Exception as e:
                print(e)
            
            
        byte = pickle.dumps( {'wins': ls } )
        return QByteArray(byte)

    def setTabPosition(self, pos):
        super(DockTab,self).setTabPosition( pos)
        index = -1
        for win in self.get_wins():
            index += 1
            title = win.windowTitle()
            if self.isNeedTurnDirection(title):
                self.setTabText(index, "")  
                
                
class TabWidget_crossDrag(QObject):
    """与bar的_crossDrag组件一起构成了Tabwidget的拖拽功能
    
    """
    drag_finish=pyqtSignal()
    drag_ing=pyqtSignal(int)
    def __init__(self, tabwidget):
        super(TabWidget_crossDrag,self).__init__(tabwidget)
        self.tabwidget = tabwidget
        tabwidget.setAcceptDrops(True)
        add_sub_obj(tabwidget, self)

    def dragEnterEvent(self, event):
        mime = event.mimeData()
        if hasattr(mime,'win'):
            event.acceptProposedAction()
        
    def dropEvent(self, event):
        mime = event.mimeData()
        self.tabwidget.addTab(mime.win, mime.win.windowTitle() ) 
        self.drag_finish.emit()
        self.tabwidget.tabBar().update()   
        
    def dragMoveEvent(self, event):
        self.drag_ing.emit(-1)  # 标识线显示在最后一个标签，表示拖过来的窗口放在最后面
        
    def dragLeaveEvent(self, event):
        self.drag_finish.emit()
        self.tabwidget.tabBar().update()  
        
        
class BarBase(QTabBar):
    """用在TabWidgetBase中，用来增加功能，比如调整中文方向，垮窗口拖动标签
    
        用在TabWidget.enableCrossDrag的参数中
    因为跨窗口拖动和调整中文方向，都需要更改QTableWidget.tabbar对象的行为，所以自定义了这个Bar，在enableXXX中会自动替换原tabbar。
    可以被继承实现更多功能
    """
    def __init__(self, p , *args):
        super(BarBase,self).__init__(p, *args)
        self.tabwidget = p
        self.tabHigh = 20
        self.comChinese = _ChineseDirection(self)
        self.comDrag = Bar_crossDrag(self)
        
        add_sub_obj(self,self.comChinese)
        add_sub_obj(self,self.comDrag)

    @sub_obj_call
    def mouseMoveEvent(self, event):
        super(BarBase,self).mouseMoveEvent(event)
    
    @sub_obj_call
    def mousePressEvent(self, event):
        super(BarBase,self).mousePressEvent(event)
    
    @sub_obj_call
    def dragMoveEvent(self, event):
        super(BarBase,self).dragMoveEvent(event)
        #self.comDrag.dragMoveEvent(event)
    
    @sub_obj_call
    def dragEnterEvent(self, event):
        self.comDrag.dragEnterEvent(event)
    
    @sub_obj_call
    def dragLeaveEvent(self, event): 
        pass
        #self.comDrag.dragLeaveEvent(event)
    
    @sub_obj_call
    def dropEvent(self, event):
        pass
        #self.comDrag.dropEvent(event)
    
    @sub_obj_call
    def paintEvent(self, event):
        super(BarBase,self).paintEvent(event)
   
        
class _ChineseDirection(QObject):
    """能够调整中文的方向"""
    def __init__(self, bar):
        self.tabwidget = bar.tabwidget
        self.bar = bar
        #self.tabwidget.isNeedTurnDirection = self.isNeedTurnDirection
        self.old_bar_tabSizeHint = self.bar.tabSizeHint
        self.bar.tabSizeHint = self.tabSizeHint
        
    #def isNeedTurnDirection(self, text):
        #if self.tabwidget.tabPosition() != QTabWidget.North:
            #if not re.match("^[A-Za-z]", text):
                #return True
        #return False 
    
    def tabSizeHint(self, index):
        win = self.tabwidget.widget(index)
        if not self.tabwidget.isNeedTurnDirection(win.windowTitle()):
            return self.old_bar_tabSizeHint(index)  
        size = QSize()
        size.setHeight(self.bar.fontMetrics().height() * len(win.windowTitle()))
        size.setWidth(25)
        size.setHeight(size.height() + 20)
        return size
    
    def paintEvent(self,event):
        painter = QPainter(self.bar)

        # 单独画中文
        for win in self.tabwidget.get_wins():
            tooltip = win.windowTitle()
            if self.tabwidget.isNeedTurnDirection(tooltip):
                rect = self.bar.tabRect(self.tabwidget.indexOf(win))
                #rect.translate(3, 8)
                rect.adjust(5,8,-5,-3)
                painter.drawText(rect, Qt.TextWordWrap , tooltip)          

class Bar_crossDrag(QObject):
    """实现自定义的垮tabwidget的拖动。其还需要tabwidget中的_crossDrag的配合"""
    def __init__(self, bar):
        super(Bar_crossDrag,self).__init__(bar)
        self.bar = bar
        self.tabwidget = bar.tabwidget
        self.bar.setAcceptDrops(True)
        self.line = None
        #add_sub_obj(self.bar, self)
    
    def clear_line(self):
        self.line=None
         
    def drawLine(self, tabIdx):
        if tabIdx == -1:
            tabIdx = self.bar.count() - 1
            rect = self.bar.tabRect(tabIdx)
            if self.tabwidget.tabPosition() == QTabWidget.North:
                self.line = ( rect.topRight(), rect.bottomRight() )
            else:   
                self.line = ( rect.bottomLeft(), rect.bottomRight() )            
        else:
            
            rect = self.bar.tabRect(tabIdx)
            if self.tabwidget.tabPosition() ==  QTabWidget.North:
                self.line = ( rect.topLeft(), rect.bottomLeft() )
            else:   
                self.line = ( rect.topLeft(), rect.topRight() )
        self.bar.update()
        
    def dragMoveEvent(self, event):
        tabIdx = self.bar.tabAt( event.pos())
        self.drawLine(tabIdx)  
        
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        
    def dragLeaveEvent(self, event):
        self.line = None
        self.bar.update()
        
    def dropEvent(self, event):
        mime = event.mimeData()
        tabIdx = self.bar.tabAt( event.pos())
        if tabIdx != -1:
            self.tabwidget.insertTab(tabIdx, mime.win, mime.win.windowTitle())
        else:
            self.tabwidget.addTab(mime.win, mime.win.windowTitle())
        
        self.line = None
        self.bar.update()
        
    def paintEvent(self, event):
        painter = QPainter(self.bar)
        # 画拖动时的线条
        if self.line:
            pen = QPen()
            pen.setColor(Qt.red)
            pen.setWidth(3)
            painter.setPen(pen)
            painter.drawLine(self.line[0], self.line[1])    
    def mousePressEvent(self, event):
        self.pressPos = event.pos()
        
    def mouseMoveEvent(self, event):
        #self = self.bar
        if not (event.buttons() & Qt.LeftButton):
            return
        if ((event.pos() - self.pressPos).manhattanLength() < QApplication.startDragDistance()):
            return      

        itemIdx = self.bar.tabAt(self.pressPos)
        if itemIdx == -1:
            return
        
        drag = QDrag(self.bar)
        mimeData = QMimeData()
        mimeData.win= self.tabwidget.widget(itemIdx)
        drag.setMimeData(mimeData)
   
        dropAction = drag.exec_(Qt.CopyAction | Qt.MoveAction) 
        
   




if __name__ == "__main__":
    import sys
    from PyQt4.QtGui import QApplication,QMainWindow,QTextEdit
    app = QApplication(sys.argv)
    man = QMainWindow()
    win = DockTab()
    #bar = Bar(win)
    #win.setTabBar(bar)
    #win.enableCrossDrag()
    #win.enableChineseDirection()
    #win.setMovable(True)
    man.setCentralWidget(win)
    man.show()    
    win.addTab(QTextEdit(), u"haha")
    win.addTab(QTextEdit(), u"中文")
    win.addTab(QTextEdit(), u"英文")
    win.setTabPosition(QTabWidget.West)
    win.setTabsClosable(True)
    
    win2 = DockTab()
    
    #bar2 = Bar(win2)
    #win2.setTabBar(bar2)
    #win2.enableCrossDrag()
    #win2.enableChineseDirection()
    win2.show()
    win2.setTabsClosable(True)
    #win2.addTab(QTextEdit(), "jjj")
    sys.exit(app.exec_())