#!python3

import os
import re

config={
    'entry':'',
    'out':'',
    'ext':['txt'],
    'exclude':['']
}

def parse(config):
    entry=config.get('entry')
    #encode=config.get('encode','utf-8')
    out= os.path.normpath(config.get('out'))
    exclude=[os.path.normpath(path) for path in config.get('exclude',[])]
    context={}
    for root,dirs,files in os.walk(entry):
        for d in list(dirs):
            next_level=os.path.normpath(os.path.join(root,d))
            if next_level==out or next_level in exclude:
                dirs.remove(d)
 
        for f in files:
            mt = re.search('\.(\w+)$',f)
            if not config.get('ext') or \
               ( mt and mt.group(1) in config.get('ext')):
                for k,v in extrac_doc(os.path.join(root,f)):
                    path_key=os.path.join(out,k)
                    context[path_key] = context.get(path_key,[])
                    context[path_key].append(v)                    
          
    doc_write(context)


   
def extrac_doc(file_path):
    with open(file_path,encoding='utf-8') as f:
        print(file_path)
        for mt in re.finditer('^\s*>>>([\w/\.]+)>(.+?)^\s*<<<<',f.read(),re.M|re.S ):
            yield (mt.group(1), mt.group(2))
        

def doc_write(context):
    for path,v in context.items():
        try:
            par = os.path.dirname(path)
            os.makedirs(par)
        except OSError:
            pass
        
        with open(path,'w',encoding='utf-8') as f:
            f.write(''.join(v))
            
if __name__=='__main__':
    #extrac_doc('d:/try/doc/test1.txt')
    #config={
        #'entry':'d:/try/doc',
        #'out':'d:/try/doc/gen',
        #'ext':['txt']
    #}
    
    config={
     'entry':'d:/coblan/webcode',
     'out':'d:/coblan/webcode/doc/source',
     'ext':['html','js'],
     'exclude':['d:/coblan/webcode/node_modules']
    }  
    
    parse(config)