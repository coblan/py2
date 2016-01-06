from heQt.qteven import *
from PyQt4.QtCore import QByteArray
from PyQt4.QtGui import QStandardItem,QStandardItemModel

def save_model(model):
    out = QByteArray()
    row,col=model.rowCount(),model.columnCount()
    for ri in range(row):
        for ci in range(col):
            if model.index(ri,ci).data():
                out.writeBool(True)
                out.writeInt32(ri)
                out.writeInt32(ci)
                out<<model.item(ri,ci)
                recurSave(model.item(ri,ci), out)
    out.writeBool(False)
    return out

def open_model(in_):
    canFetch=in_.readBool()
    while canFetch:
        tmp=QStandardItem()
        ri,ci=in_.readInt32(),in_.readInt32()
        in_>>tmp
        model.setItem(ri,ci,tmp)
        recurOpen(tmp, in_)
        canFetch=in_.readBool()

if __name__ =='__main__':
    model = QStandardItemModel()
    model.appendRow(QStandardItem('dd'))
    jj=save_model(model)
    print(jj)