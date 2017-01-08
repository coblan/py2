# -*- encoding: utf-8 -*-  
  
from django.conf import settings  
import os.path  
settings.configure(  
    TEMPLATE_LOADERS = (  
        'django.template.loaders.filesystem.Loader',  
    ),  
    TEMPLATE_DIRS = ( os.path.dirname(__file__) ,)
)  
      # 在当前路径搜索模板文件  
from django.template import loader, Context  
t = loader.get_template('demo.tpl') # demo.tpl必须与该代码在同一目录，文件内容见下一段代码  
context_dict = {  
    'name' : 'Jim',  
    'gender' : 'Male',  
    'age' : '18',  
}  
c = Context(context_dict)  
print t.render(c)  