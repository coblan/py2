import numpy as np
from pandas import Series,DataFrame
import pandas

import json

db=json.load(open( 'd:/try/pandas_data/foods-2011-10-03.txt') )

nut=DataFrame(db[0].get('nutrients'))
infokeys = ['description','group','id','manufacturer']
info = DataFrame(db,columns= infokeys)

nutrients=[]
for rec in db:
    fnuts=DataFrame(rec['nutrients'])
    fnuts['id']=rec['id']
    nutrients.append(fnuts)
nutrients=pandas.concat(nutrients,ignore_index=True)

col_mapping={'description':'food','group':'fgroup'}
info = info.rename(columns=col_mapping,copy=False)

ndata=pandas.merge(nutrients,info,on='id',how='outer')
result=ndata.groupby(['nutrient','fgroup'])['value'].quantile(0.5)