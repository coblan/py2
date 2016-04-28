# -*- encoding:utf-8 -*-

import os.path

"""
"""
def print_directory_content(path):
    for r,dirs,files in walk(path):
        for dir in dirs:
            print(os.path.join(r,dir))
        for file in files:
            print(os.path.join(r,file))



def walk(dir_):
    out=__req(dir_)
    if out:
        yield out
        dirs=out[1]
        for ii in dirs:
            for jj in  walk(os.path.join(out[0],ii),except_):
                yield jj          


def __req(dir_):
    if not dir_:
        return
    ls=os.listdir(dir_)
    root=dir_
    dirs=[]
    files=[]
    for ii in ls:
        if os.path.isdir(os.path.join(root,ii)):
            dirs.append(ii)
        else:
            files.append(ii)
    return (root,dirs,files)



if __name__ =='__main__':
    print_directory_content('../exam')