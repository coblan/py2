from heQt.qteven import *
from PyQt4.QtCore import QByteArray
from PyQt4.QtGui import QStandardItem,QStandardItemModel
from stditem import save_item,save_dsd,load_item,load_dsd
import pickle

def save_model(model):
    row,col=model.rowCount(),model.columnCount()
    childs =[]
    for ri in range(row):
        for ci in range(col):
            if model.index(ri,ci).data():
                item=model.item(ri,ci)
                childs.append({
                    'r':ri,
                    'c':ci,
                    'item':save_item(item),
                    'dsd':save_dsd(item)
                })

    return childs


def load_model(model,childs):
    for child in childs:
        r=child.get('r')
        c=child.get('c')
        item=load_item(child.get('item'))
        model.setItem (r, c, item)
        load_dsd(item,child.get('dsd'))
    return model



if __name__ =='__main__':
    model = QStandardItemModel()
    model.appendRow(QStandardItem('dd'))
    jj=save_model(model)
    print(jj)
    model2 = QStandardItemModel()
    k=load_model(model2,jj)
    print(k.rowCount())