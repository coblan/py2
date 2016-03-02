# -*- encoding:utf8 -*-
from heQt.qteven import *
from PyQt4.QtCore import QByteArray,QDataStream,QIODevice
from PyQt4.QtGui import QStandardItem

def save_item(item):
    byt=QByteArray()
    out=QDataStream(byt,QIODevice.WriteOnly)
    #item.write(out)
    out<<item
    return byt

def save_dsd(item):
    """
    保存子孙为 [{}]
    """
    if not item:
        return
    row,col=item.rowCount(),item.columnCount()
    childs=[]
    for ri in range(row):
        for ci in range(col):
            child=item.child(ri,ci)
            childs.append({
                'r':ri,
                'c':ci,
                'item':save_item(child),
                'dsd':save_dsd(child)
            })
        
    return childs

def load_item(qbyte):
    item=QStandardItem()
    in_=QDataStream(qbyte,QIODevice.ReadOnly)
    in_>>item
    return item

def load_dsd(parent,childs):
    """加载子孙item
    """
    for child in childs:
        r=child.get('r')
        c=child.get('c')
        child_item=load_item(child.get('item'))
        parent.setChild(r,c,child_item)
        load_dsd(child,child.get('dsd'))
    return parent
        

if __name__ =='__main__':
    from PyQt4.QtCore import Qt
    h=QStandardItem('has')
    print(h.data(Qt.DisplayRole))
    f=save_item(h)
    print(f)
    k=load_item(f)
    print(k.data(Qt.DisplayRole))