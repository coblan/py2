# -*- encoding:utf8 -*-
from heQt.qteven import *
import sys
import os
from subprocess import Popen
from string import Template
from PyQt4.QtGui import QTreeView, QStandardItemModel, QSplitter, QMessageBox, QApplication, QTextEdit, QStandardItem
from PyQt4.QtCore import QObject, Qt, QSettings, QModelIndex


class Logic(QObject):
    def __init__(self, tree_, info_):
        super(Logic, self).__init__()
        # assert isinstance(self.info, QTextEdit)
        self.tree = tree_
        self.info = info_

    def add(self):
        idx = self.tree.ctxMenuIdx
        self.tree.model().append(QStandardItem('new item'), idx if idx else None)

    def delete(self):
        idx = self.tree.ctxMenuIdx
        if idx.isValid():
            if QMessageBox.information(None, 'warn', 'realy delete?%s' % idx.data()) == QMessageBox.Ok:
                self.tree.model().remove(idx)

    def run(self):
        scope = {}
        exec (self.info.toPlainText(), scope)
        cmd = scope.get("cmd", "can'g find cmd!")
        f = open('tmp.bat', 'w')
        if 'var' in scope:
            cmd = Template(cmd).substitute(scope["var"])

        f.write(cmd)
        f.close()
        Popen('cmd /k %s/tmp.bat' % os.getcwd(), universal_newlines=True)

    def save(self):
        idx = self.tree.currentIndex()
        self.tree.model().itemFromIndex(idx).setData(self.info.toPlainText(), Qt.UserRole + 1)
        self.tree.model().save('confing')


class TreeView(QTreeView):
    index_changed = Signal(QModelIndex, QModelIndex)

    def __init__(self, parent=None):
        super(TreeView, self).__init__(parent)
        self.setModel(QStandardItemModel())

    def currentChanged(self, cur, pre):
        self.index_changed.emit(cur, pre)
        return super(TreeView, self).currentChanged(self, cur, pre)


class CmdWin(QSplitter):
    def __init__(self, *args, **kwargs):
        super(CmdWin, self).__init__(*args, **kwargs)
        self.setWindowTitle(u'命令行界面版')
        self.tree = TreeView()
        self.info = QTextEdit()
        self.auOb = Logic(self.tree, self.info)
        self.addWidget(self.tree)
        self.addWidget(self.info)
        self.tree.index_changed.connect(self.on_tree_index_changed)

    def on_tree_index_changed(self, cur, pre):
        """

        @type cur: QModelIndex
        @type pre: QModelIndex
        """
        if pre.isValid():
            self.tree.model().itemFromIndex(pre).setData(self.info.toPlainText(), Qt.UserRole + 1)
        self.info.setPlainText(cur.data(Qt.UserRole + 1))


    def load_settings(self):
        try:
            stns = QSettings('stns', QSettings.IniFormat)
            self.restoreGeometry(stns.value('win/geo'))
            self.restoreState(stns.value("win/split"))
        except TypeError:
            pass

    def closeEvent(self, evnt):
        stns = QSettings('stns', QSettings.IniFormat)
        stns.setValue('win/geo', self.saveGeometry())
        stns.setValue("win/split", self.saveState())
        super(CmdWin, self).closeEvent(evnt)


if __name__ == '__main__':
    os.chdir('cmdgui')
    app = QApplication(sys.argv)
    mainWin = CmdWin()

    # lay=QSplitter()

    # tree = TreeView()
    # info = QTextEdit()
    # auOb = aux(tree, info)
    # tree.info = info
    # mode = treeModel(None)
    # mode.open('confing')
    #
    # tree.setModel(mode)
    #
    # tree.addAction('run').triggered.connect(auOb.run)
    # act = QAction(None)
    # act.setSeparator(True)
    # tree.addAction(act)
    # tree.addAction('add').triggered.connect(auOb.add)
    # tree.addAction('delete').triggered.connect(auOb.delete)
    #
    # tree.addAction('save').triggered.connect(auOb.save)
    #
    # mainWin.addWidget(tree)
    # mainWin.addWidget(info)

    # mainWin.setLayout(lay)
    mainWin.show()
    mainWin.load_settings()

    sys.exit(app.exec_())
