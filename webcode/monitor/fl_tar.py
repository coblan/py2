# encoding:utf-8

import tarfile  
import os  

def tgz(dir_path):
    tar = tarfile.open(dir_path+".tar.gz", "w:gz")
    tar.add(dir_path)
    tar.close()    

def un_tgz(file_path):
    tar=tarfile.open(file_path)
    # dir_path = file_path.replace(".tar.gz", "")
    dir_path=os.path.dirname(file_path)
    tar.extractall(dir_path)
    tar.close()    


if __name__=='__main__':

    # un_tgz("keys.tar.gz")
    tgz('data')

    
