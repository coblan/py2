from heQt.qteven import *
import pickle
import re
from qt_.widget.tabWidget_.barBase import BarBase
from struct_.cls import sub_obj_call, add_sub_obj

class TabWidgetBase(QTabWidget):
    """
    默认向QTabWidget增加的功能：
    1 迭代窗口a
    2 保存，恢复所有能够pickle的窗口
    
    可以开启功能：
    1 enableCrossDrag   自定义的拖动。可以垮Tabwidget拖动
    2 enableChineseDirection  中文旋转 。利用自绘中文来实现。
                              如果还需要拖动，最好开启"1 自定义拖动"，因为Qt自带拖动，自绘标签有空白。
    
    """
    def __init__(self, *args):
        super(TabWidgetBase,self).__init__( *args)
        self.bar=cusBar(self)
        self.setTabBar(self.bar)
        self.bar.enable_chinese_direction()
        
        self.tabCloseRequested.connect(self.removeTab)

    #def enableCrossDrag(self, cusBar = BarBase):
        #"""注意：cusBar是BarBase<-Bar的子类，**不是** 类对象"""
        #if not hasattr(self, "cusBar"):
            #self.cusBar = cusBar(self)
            #self.setTabBar(self.cusBar)
        #self.cusBar.enableCrossDrag()
        #self.crossDrag = _crossDrag(self, self.cusBar.comDrag)
        
    #def enableChineseDirection(self, cusBar = BarBase):
        #if not hasattr(self, "cusBar"):
            #self.cusBar = cusBar(self)
            #self.setTabBar(self.cusBar) 
        #self.cusBar.enableChineseDirection()
        
    #@sub_obj_call
    #def dragEnterEvent(self, event):
        #pass
    
    #@sub_obj_call
    #def dropEvent(self, event):
        #pass 
    
    #@sub_obj_call
    #def dragMoveEvent(self, event):
        #super().dragMoveEvent(event)
        
    #@sub_obj_call
    #def dragLeaveEvent(self, event):
        #pass   
    
    ##[1] 迭代窗口
    #def __iter__(self):
        #self.iterIndex=-1
        #return self    
    #def __next__(self):
        #self.iterIndex += 1
        #if self.iterIndex < self.count():
            #return self.widget( self.iterIndex )
        #raise StopIteration    
    
    #[2] 添加窗口，添加标签名，将名字标签名保存在windowTitle中
    def addTab(self, widget, name_icon = "", name = ""):
        widget.tabWidget_ = self
        if isinstance(name_icon, QIcon):
            widget.setWindowTitle(name)
            if self.isNeedTurnDirection(name):
                return super().addTab(widget, name_icon)
            else:
                return super().addTab(widget, name_icon, name)
        else:
            widget.setWindowTitle(name_icon)
            if self.isNeedTurnDirection(name_icon):
                return super().addTab(widget, "")
            else:
                return super().addTab(widget, name_icon)
            
    def isNeedTurnDirection(self, text):
        if self.tabPosition() != QTabWidget.North:
            if re.search(u'[\u4e00-\u9fa5]+',text):
                return True
            #if not re.match("^[A-Za-z]", text):
                #return True
        return False   
    
    def insertTab(self, index, widget, name_icon , name = None):
        widget.tabWidget_ = self
        if isinstance(name_icon, QIcon):
            widget.setWindowTitle(name)
            if self.isNeedTurnDirection(name):
                super().insertTab(index, widget, name_icon)
            else:
                super().insertTab(index, widget, name_icon, name)
        else:
            widget.setWindowTitle(name_icon)
            if self.isNeedTurnDirection(name_icon):
                super().insertTab(index, widget, "")
            else:
                super().insertTab(index, widget, name_icon)    
                
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
        for win in self:
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

    def isNeedTurnDirection(self, text):
        """sub_obj .hook 函数"""
        return False

    def setTabPosition(self, pos):
        super().setTabPosition( pos)
        index = -1
        for win in self:
            index += 1
            title = win.windowTitle()
            if self.isNeedTurnDirection(title):
                self.setTabText(index, "")    
        
class BarBase(QTabBar):
    """用在TabWidgetBase中，用来增加功能，比如调整中文方向，垮窗口拖动标签"""
    def __init__(self, p , *args):
        super(BarBase,self).__init__(p, *args)
        self.tabwidget = p
        self.tabHigh = 20

    def enableChineseDirection(self):
        self.comChinese = _ChineseDirection(self)
        #add_sub_obj(self, self.comChinese)
    
    def enableCrossDrag(self):
        self.comDrag = _crossDrag(self)
        self.comDrag.install()
       
 
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        
    @sub_obj_call
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
    @sub_obj_call      
    def dragMoveEvent(self, event):
        super().dragMoveEvent(event)
    @sub_obj_call
    def dragEnterEvent(self, event):
        pass
    @sub_obj_call
    def dragLeaveEvent(self, event): 
        pass
    @sub_obj_call
    def dropEvent(self, event):
        pass
    @sub_obj_call
    def paintEvent(self, event):
        super().paintEvent(event)
        if hasattr(self,'comChinese'):
            self.comChinese.paint()
        
        
class _ChineseDirection(QObject):
    """能够调整中文的方向"""
    def __init__(self, bar):
        self.tabwidget = bar.tabwidget
        self.bar = bar
        self.tabwidget.isNeedTurnDirection = self.isNeedTurnDirection
        self.old_bar_tabSizeHint = self.bar.tabSizeHint
        self.bar.tabSizeHint = self.tabSizeHint
        
    def isNeedTurnDirection(self, text):
        if self.tabwidget.tabPosition() != QTabWidget.North:
            if not re.match("^[A-Za-z]", text):
                return True
        return False   
    def tabSizeHint(self, index):
        win = self.tabwidget.widget(index)
        if not self.isNeedTurnDirection(win.windowTitle()):
            return self.old_bar_tabSizeHint(index)  

        size = QSize()
        size.setHeight(self.bar.fontMetrics().height() * len(win.windowTitle()))
        size.setWidth(20)
        size.setHeight(size.height() + 20)
        return size
    
    def paint(self):
        painter = QPainter(self.bar)

        # 单独画中文
        for win in self.tabwidget:
            tooltip = win.windowTitle()
            if self.isNeedTurnDirection(tooltip):
                rect = self.bar.tabRect(self.tabwidget.indexOf(win))
                rect.translate(3, 8)
                painter.drawText(rect, Qt.TextWordWrap , tooltip)          

class _crossDrag:
    """实现自定义的垮tabwidget的拖动。其还需要tabwidget中的_crossDrag的配合"""
    def __init__(self, bar):
        self.bar = bar
        self.tabwidget = bar.tabwidget
    def install(self):
        self.bar.setAcceptDrops(True)
        self.line = None
        add_sub_obj(self.bar, self)
        
    def dragMoveEvent(self, event):
        tabIdx = self.bar.tabAt( event.pos())
        self.drawLine(tabIdx)
        
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
        self.bar.pressPos = event.pos()
    def mouseMoveEvent(self, event):
        self = self.bar
        if not (event.buttons() & Qt.LeftButton):
            return
        if ((event.pos() - self.pressPos).manhattanLength() < QApplication.startDragDistance()):
            return      

        itemIdx = self.tabAt(self.pressPos)
        if itemIdx == -1:
            return
        
        drag = QDrag(self)
        mimeData = QMimeData()
        mimeData.win= self.tabwidget.widget(itemIdx)
        drag.setMimeData(mimeData)
   
        dropAction = drag.exec_(Qt.CopyAction | Qt.MoveAction) 
        
class _crossDrag:
    """与bar的_crossDrag组件一起构成了Tabwidget的拖拽功能"""
    def __init__(self, tabwidget, bar_comdrag):
        self.tabwidget = tabwidget
        tabwidget.setAcceptDrops(True)
        add_sub_obj(tabwidget, self)
        self.bar_comdrag = bar_comdrag
        
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
    def dropEvent(self, event):
        mime = event.mimeData()
        self.tabwidget.addTab(mime.win, mime.win.windowTitle() ) 
        self.bar_comdrag.line = None
        self.tabwidget.tabBar().update()   
        
    def dragMoveEvent(self, event):
        self.bar_comdrag.drawLine( -1)
    def dragLeaveEvent(self, event):
        self.bar_comdrag.line = None
        self.tabwidget.tabBar().update()     

from qt_.qtEven import *
from qt_.widget.tabWidget_.barBase import BarBase
from qt_.widget.tabWidget_.tabWidgetBase import TabWidgetBase
import pickle, re
class TabWidget(TabWidgetBase):
    """
    默认增加功能：
    1 迭代窗口
    2 保存，恢复所有能够pickle的窗口
    
    重要函数：
    enableCrossDrag(Bar<-cls)           开启夸窗口拖拽功能
    enableChineseDirection(Bar<-cls)    开启中文调整方向功能
    
    注意：这两个函数的参数是Bar的子类，不是Bar的对象
    """
    pass
class Bar(BarBase):
    """
    用在TabWidget.enableCrossDrag的参数中
    因为跨窗口拖动和调整中文方向，都需要更改QTableWidget.tabbar对象的行为，所以自定义了这个Bar，在enableXXX中会自动替换原tabbar。
    可以被继承实现更多功能
    """
    pass
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    man = QMainWindow()
    win = TabWidget()
    #bar = Bar(win)
    #win.setTabBar(bar)
    win.enableCrossDrag()
    win.enableChineseDirection()
    #win.setMovable(True)
    man.setCentralWidget(win)
    man.show()    
    win.addTab(QTextEdit(), "haha")
    win.addTab(QTextEdit(), "中文")
    win.addTab(QTextEdit(), "英文")
    win.setTabPosition(QTabWidget.West)
    win.setTabsClosable(True)
    
    win2 = TabWidget()
    
    #bar2 = Bar(win2)
    #win2.setTabBar(bar2)
    win2.enableCrossDrag()
    win2.enableChineseDirection()
    win2.show()
    win2.setTabsClosable(True)
    #win2.addTab(QTextEdit(), "jjj")
    sys.exit(app.exec_())