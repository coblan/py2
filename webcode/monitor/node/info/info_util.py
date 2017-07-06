import csv
import os
from datetime import datetime
       
def append(dc,path):
    """
    dc={'date':'xxx','f1':'xx','f2':'xxx'}
    """
    try:
        os.makedirs(os.path.dirname(path))
    except Exception:
        pass
    
    head=[key for key in dc.keys()]
    head.sort()
    
    row=[dc[key] for key in head]
    
    head=['datetime']+head
    now=datetime.now()
    row=[now.strftime('%Y-%m-%d %H:%M:%S')]+row
    
    has_header=False
    if os.path.exists(path):
        with open(path,'rb') as f:
            if f.readline():
                has_header=True

    with open(path,'a+b') as f:
        writer = csv.writer(f)
        if not has_header:
            writer.writerow(head)
        writer.writerow(row)
        


