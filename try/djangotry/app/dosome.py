import os
os.environ[' DJANGO_SETTINGS_MODULE']='mysettings'
#import settings

from models import MyModel

myModel = MyModel()  
myModel.name = 'Jim Green'  
myModel.gender = True  
myModel.age = 18  
myModel.save()