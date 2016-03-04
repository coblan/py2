# -*- encoding:utf8 -*-

from heQt.qteven import *
from PyQt4.QtGui import QSplitter,QTabWidget,QAction,QMenu
from PyQt4.QtCore import Qt,QByteArray
from drap_tree import DockTab,BarBase
import pickle

class Dock(QSplitter):
    """
    Dock是DockPanel的容器，DockPanel是toolTab的容器，toolTab时QWidget子类，放置各种工具的页面
    Dock类，具有左中右三个位置，用于放置DockPannel面板。这些面板可以随意拖拽。
例子:
    mainWin=QMainWindow()
    mainWin.dock=Dock()
    mainWin.setCentralWidget(mainWin.dock)
    mainWin.dock.setCentralWidget( QWidget() )  # 你自己的QWidget
    
    # DockPanel的位置可以是左中右三种
    mainWin.panel1=DockPanel()
    mainWin.dock.addLeft( mainWin.panel1)
    
    # DockPanel.addTab()添加QWidget对象，工具页面
    mainWin.panel1.addTab(win)
    
功能：
    1.保存功能:
        如果要求DockPanel中的工具页面能够保存，下次启动时能够自动回复，就必须实现其pickle接口
    
    2.工具页面tabbar上的邮件菜单:
       *. toolTab实现函数tabbarAction()，其返回QAction的列表
       *. DockPanel.actions()
    
    """    
    def __init__(self, *args):
        super(Dock,self).__init__( *args)
        self.left = QSplitter(Qt.Vertical)
        self.middle = QSplitter(Qt.Vertical)
        self.right = QSplitter(Qt.Vertical)   
        
        self.left.added = False
        #self.addWidget(self.left)
        self.addWidget(self.middle)
        self.right.added = False
        #self.addWidget(self.right)        

        self.middle.addWidget(QLabel("middle"))
        self.middle.split = QSplitter()
        #self.middle.setStretchFactor(0, 1)
        #self.middle.setStretchFactor(1, 0)
        self.middle.split.added = False
        #self.middle.addWidget(self.middle.split)  

        #self.setStretchFactor(0, 0)
        #self.setStretchFactor(1, 1)
        #self.setStretchFactor(2, 0)        

        self.setChildrenCollapsible(False)

        self.left.openedWidth = 30
        self.right.openedWidth = 30
        self.middle.split.openedWidth = 30         

        self.left.p_spit = self
        self.right.p_spit = self
        self.middle.split.p_spit = self.middle

        #def updateStretchFactor(self):
        #if self.
        #self.setStretchFactor(0, 0)
        #self.setStretchFactor(1, 1)
        #self.setStretchFactor(2, 0)           
    def addLeft(self, tabWin):
        if not self.left.added:
            self.insertWidget(0, self.left)
            self.left.added = True

        tabWin.install(self.left, self, QTabWidget.East)
        return tabWin

    def addRight(self,  tabWin):
        if not self.right.added:
            self.addWidget( self.right)
            self.right.added = True        
        tabWin.install(self.right, self, QTabWidget.West)
        return tabWin
    def addMiddle(self, tabWin):
        if not self.middle.split.added:
            self.middle.addWidget( self.middle.split)
            self.middle.split.added = True 
            self.middle.setStretchFactor(0, 1)
            self.middle.setStretchFactor(1, 0) 

        tabWin.install(self.middle.split, self.middle, QTabWidget.North)
        return tabWin
    def setCentralWidget(self, win):
        self.middle.widget(0).setParent(None)
        self.middle.insertWidget(0, win)
        self.middle.setStretchFactor(0, 1)
        self.middle.setStretchFactor(1, 0)
        
    # def __reduce__(self):
        # dc={'state':self.saveDock()}
        # return self.__class__, tuple() ,dc
    
    # def __setstate__(self,state):
        # self.restoreDock(state['state'])
        
    def save(self):
        state = {}
        state["state"] = self.saveState()
        state["left"] = self._saveSplit(self.left)
        state["middle"] = self._saveMiddle()
        state["right"] = self._saveSplit(self.right)
        return pickle.dumps(state)
    
    def restore(self, state):
        # if not QByt:
            # return
        # if isinstance(QByt, QByteArray):
            # QByt = QByt.data()
        state = pickle.loads(state)
        self._restoreSplit(state, self.addLeft, "left")
        self._restoreSplit(state, self.addRight, "right")
        self._restoreMiddle(state)

        self.restoreState(state.get("state", None))   

    def _saveSplit(self, split):
        dc = {"state" : split.saveState()}
        ls = []
        for i in range(split.count()):
            win = split.widget(i)
            ls.append(win)     
        dc["wins"] = ls
        dc["openedWidth"] = split.openedWidth
        return dc
    
    def _saveMiddle(self):
        dc = {"state" : self.middle.saveState()}
        dc["state1"] = self.middle.split.saveState()
        ls = []
        for i in range(self.middle.split.count()):
            win = self.middle.split.widget(i)
            ls.append(win)     
        dc["wins"] = ls 
        dc["openedWidth"] = self.middle.split.openedWidth
        return dc

    def _restoreMiddle(self, state):
        dc = state.get("middle", None)
        if dc:
            for win in dc["wins"]:
                self.addMiddle(win)
            self.middle.split.restoreState(dc.get("state1", None))
            self.middle.restoreState(dc.get("state", None))
            self.middle.split.openedWidth = (dc.get("openedWidth", 100))
    def _restoreSplit(self, state, fun, name):
        innState = state.get(name, None)  
        if innState:
            for win in innState["wins"]:
                fun(win)
            getattr(self, name).restoreState(innState["state"])   
            getattr(self, name).openedWidth = innState.get("openedWidth", 100)



class DockPanel(DockTab):
    """
      放在DockWidget中的标签页的容器
    开启了TabWidget的中文调整方向，自定义拖拽功能
    增加了点击标签切换开关。该功能主要在TabWidget.Bar<- customBar类中实现。
    
    """
    postion = [QTabWidget.North, QTabWidget.South, QTabWidget.East, QTabWidget.West]
    def __init__(self, *args):
        super(DockPanel,self).__init__( *args)
        self.setTabBar(customBar(self))
        self.setMinimumWidth(20)
        self.setMinimumHeight(20)
        self.setAcceptDrops(True)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        act_rm_tab=QAction(u'移除当前标签页',self)
        act = QAction(u"移除本面板", self)
        
        self.addAction(act_rm_tab)
        self.addAction(act)
        
        act_rm_tab.triggered.connect(self.remove_current_tab)
        act.triggered.connect(self.uninstall)
    
    def remove_current_tab(self):
        self.removeTab(self.currentIndex())
    
    def uninstall(self):
        ls = []
        for win in self.get_wins():
            ls.append(win)
        for win in ls:
            if hasattr(win, "uninstall"):
                win.uninstall()
       
        p = self.parentWidget()
        self.setParent(None)
        if not p.count():
            p.setParent(None)
            p.added = False

                
    def install(self, splitter, outterSplit, pos):
        self.splitter = splitter
        self.tabBar().mainSplit = outterSplit
        self.tabBar().tabWidget = self
        
        self.grandParSplitter = outterSplit
        if splitter.orientation() == Qt.Vertical:
            #ls = [QTabWidget.East, QTabWidget.North, QTabWidget.West]
            #self.setTabPosition(ls[index])
            self.setTabPosition(pos)
            
        #self.tabBar().index = index
        self.tabBar().outSplit = splitter
        
        splitter.addWidget(self)
   
    # pickle 支持
    def __reduce__(self):
        wins=[]
        for win in self.get_wins():
            try:
                wins.append(pickle.dumps(win))
            except Exception as e:
                print(e)
                
        self.pickleDict = {"wins": wins, 
                           "position": self.postion.index(self.tabPosition()), 
                           "objectName": self.objectName(),}
        return self.__class__,tuple(),self.pickleDict
    
    def __setstate__(self, state):
        self.setObjectName(state["objectName"])
        wins = state.get("wins")
        for win in wins:
            win_obj = pickle.loads(win)
            self.addTab(win_obj,win_obj.windowTitle())
        self.setTabPosition(self.postion[ state.get("position", 0) ])
        # if wins:
            # self.restoreWins(wins)


class customBar(BarBase):
    """增加点击激活标签，隐藏相应的面板  的功能"""
    #def __init__(self,  *args):
        #super().__init__( *args)
        #self.clickOnActive = False

    def contextMenuEvent(self, event):
        pos = event.globalPos ()
        menu = QMenu()
        win = self.tabwidget.widget( self.tabAt(event.pos () ) )
        if hasattr(win, "tabbarAction"):
            menu.addActions(win.tabbarAction())
        menu.addActions(self.tabwidget.actions())
        menu.exec_(pos)
    
    # def current_tab(self):
        # # return self.tabwidget.widget( self.tabAt(event.pos () ) )
        # return self.tabwidget.currentWidget()
    
    def switchPanel(self):
        wid = self.mainSplit.sizes()
        index = self.mainSplit.indexOf(self.outSplit)
        if index == 0:
            absorb_index = 1
        elif index == 1:
            absorb_index = 0
        elif index == 2:
            absorb_index = 1
            
        if wid[index] <= self.tabHigh:
            #wid[index] = self.tabwidget.parentWidget().openedWidth
            wid[index] = self.outSplit.openedWidth
            wid[absorb_index] -= (self.outSplit.openedWidth - self.tabHigh)
        else:
            #self.tabwidget.parentWidget().openedWidth = wid[index]
            self.outSplit.openedWidth = wid[index]
            wid[absorb_index] += ( wid[index] - self.tabHigh)
            wid[index] = self.tabHigh
            
        self.mainSplit.setSizes(wid) 
    def mousePressEvent(self, event):
        pos = event.pos()
        self.shouldSwitch = False
        if self.currentIndex() == self.tabAt(pos) and event.button() == Qt.LeftButton :             
            self.shouldSwitch = True                          # self.shouldSwitch 的存在是因为切换标签是在mousePressEvent完成
        super(customBar,self).mousePressEvent(event)                         # "开关面板"，是在mouseReleaseEvent中完成，所以必须在mousePressEvent
        self.pressed = True                                    # 中记录下是否应该"开关面板"。
    def mouseReleaseEvent(self, event):
        if self.shouldSwitch :
            self.switchPanel()
        else:
            super(customBar,self).mouseReleaseEvent(event)



############################
#  测试代码
#############################
from PyQt4.QtGui import QLabel

class Lab(QLabel):
    def __init__(self, *args):
        super(Lab,self).__init__( *args)
        self.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.addAction(QAction("fff", self))
        
    def install(self, tab):
        tab.addTab(self, "haha")
        
    def __reduce__(self):
        self.pickleDict = {"text": self.text(),'title':self.windowTitle()}
        return self.__class__,tuple(),self.pickleDict
    
    def __setstate__(self, state):
        self.setWindowTitle(state['title'])
        self.setText(state.get("text", None))
        
    def tabbarAction(self):
        return [QAction('jjjj',self),QAction('ffff',self)]
        
def test():
    tt, ok = QInputDialog.getText(None, "s", "f")
    if not ok:
        return
    tab = DockPanel ()
    
    tab.addTab(Lab("middle"), u"当前目录")
    tab.addTab(Lab("middle"), u"大纲")
    tab.addTab(Lab('dog'), "can't save ")
    getattr(win, tt)(tab)
    
    win2=Dock()
    win2.restore(win.save())
    win2.show()
    win.brother=win2
    # ss=pickle.dumps(win)
    # tab2=pickle.loads(ss)
    # tab2.show()
    # win.brother=tab2
    # print(ss)
    
if __name__ == "__main__":

    import sys
    from PyQt4.QtGui import QMainWindow,QApplication,QPushButton,QInputDialog,QWidget
    app = QApplication(sys.argv)
    mainWin = QMainWindow()
    # mainWin.enableSaveSession()
    
    win = Dock()
    mainWin.setCentralWidget(win)
    mainWin.show()
    
    btn = QPushButton("cli")
    btn.clicked.connect(test)
    btn.show()
    
    
    #tab = DockTab()
    #tab.addTab(QWidget(), "hhh")
    #tab.addTab(QWidget(), "jjhh")
    #win.addLeft(tab)
    
    #tab2 = DockTab()
    #tab2.addTab(QWidget(), "hhh")
    #tab2.addTab(QWidget(), "jjhh")    
    
    #win.addMiddle(tab2)
    
    # mainWin.registeSaveItem(win.restoreDock, win.saveDock, "dock")
    
    # mainWin.restoreAll()
    sys.exit(app.exec_())