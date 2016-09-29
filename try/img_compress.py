from PIL import Image
# b = Book.objects.get(title='Into the wild')
# image = Image.open(r'D:\try\image\Koala.jpg')
# image.save(r'D:\try\image\Koala3.jpg',quality=5,optimize=True)
import os
import shutil
path = r'D:\work\relay\content'
dst_path = r'D:\work\relay\content2'

ioerrors = []
others = []
sizes=[]
for rt,dr,fl in os.walk(path):
    
    for f in fl:
        abs_path = os.path.join(rt,f)
        
        rel = os.path.relpath(rt,path)
        dst_root = os.path.join(dst_path,rel) 
        
        try:
            os.makedirs(dst_root)
        except os.error:
            pass        
        
        dst_abs_path = os.path.join(dst_root,f)
        print(dst_abs_path)
        if f.lower().endswith(('jpg','png')):
            sizes.append((abs_path,os.path.getsize(abs_path)))
            try:
                image = Image.open(abs_path)
                img2= image.convert('P', palette=Image.WEB,colors=64)
                img2.save(dst_abs_path,quality=60,optimize=True)
                
            except IOError:
                ioerrors.append(abs_path)
            
        else:
            others.append(abs_path)
            shutil.copy2(abs_path, dst_abs_path)
            

print('='*30)
for path in ioerrors:
    print(path)

print('+'*30)
for path in others:
    print(path)
    
# print('+'*30)
# sizes.sort(cmp=lambda x,y : cmp(y[1],x[1]))
# for path , size in sizes:
    # print(path,size)
