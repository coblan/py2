# encoding: utf-8  

import tarfile  
import os   
import argparse
import wingdbstub

parser = argparse.ArgumentParser()
parser.add_argument('-s','--source', help="file path t")
parser.add_argument('operation',help='operation')
args = parser.parse_args()
if not args.source:
    args.source='/pypro/first/first/'
    
    
def tar_src():
    tar=tarfile.open('your.tar.gz','w:gz')
    tar.add(args.source,arcname='first', exclude=exclude)
    tar.close()  

def exclude(file_name):
    if file_name.endswith('.pyc'):
        return True
    if file_name==os.path.join(args.path,'media'):
        return True
    if file_name==os.path.join(args.path,'pub_static'):
        return True
    return False

def tar_open():
    tar=tarfile.open('your.tar.gz','r:gz')
    tar.extractall(path=r"d:\try")


if __name__=='__main__':
    if args.operation=='tar':
        tar_src()
    if args.operation=='untar':
        tar_open()