# encoding: utf-8  

import tarfile  
import os   
# import argparse
# import wingdbstub
import sys

# parser = argparse.ArgumentParser()
# parser.add_argument('-s','--source', help="file path t")
# parser.add_argument('-t','--target',help='target file')
# parser.add_argument('operation',help='operation')
# args = parser.parse_args()

# if not args.source:
    # print('need source directory')
    # sys.exit(2)
# if not args.target:
    # print('need target file')
    # sys.exit(2)


def get_arg():
    class Arg(object):
        pass    
    args=Arg()
    if sys.argv:
        args.operation=sys.argv[1]
        if args.operation=='tar':
            args.source=sys.argv[2]
            args.target=sys.argv[3]
        elif args.operation=='untar':
            args.syst=sys.argv[2]
            args.target=sys.argv[3]   
    return args
    
    
def tar_src(src,target):
    tar=tarfile.open('%s.tar.gz'%target,'w:gz')
    for f in os.listdir(src):
        if f in ['venv','.localpython','exported_apps']:
            continue
        tar.add(os.path.join(src,f),arcname=f, exclude=exclude)
    tar.close()  

def exclude(file_name):
    if file_name.endswith('.pyc'):
        return True
    # if file_name==os.path.join(args.path,'media'):
        # return True
    # if file_name==os.path.join(args.path,'pub_static'):
        # return True
    return False

def tar_open(prefix,dest):
    src=_get_last_file(prefix)
    _tar_open(src,dest)
    
def _tar_open(src,dest):
    tar=tarfile.open(src,'r:gz')
    tar.extractall(path=dest,)

def _get_last_file(prefix):
    """get newest tar file in the server"""
    new=''
    for f in os.listdir('.'):
        if f.startswith(prefix) and f.endswith('tar.gz') and f>new:
            new=f
    return new


if __name__=='__main__':
    args=get_arg()
    if args.operation=='tar':
        tar_src(args.source,args.target)
    if args.operation=='untar':
        tar_open(args.syst,args.target)
    
    # tar_src('../mt','../jj')
    # _tar_open(src='../jj.tar.gz', dest='../forjj')