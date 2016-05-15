from pandas import Series, DataFrame
import pandas as pd

obj = Series([4, 7, -5, 3])
sdata = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
obj3 = Series(sdata)
states = ['California', 'Ohio', 'Oregon', 'Texas']
obj4 = Series(sdata, index=states) 
print(obj4)
data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}
frame = DataFrame(data, columns=['year', 'state', 'pop'])
print(frame)