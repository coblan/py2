#-*- encoding:utf8 -*-
from ctypes import *
import os.path
Shlwapi=WinDLL('Shell32.dll')
FO_DELETE=3
FOF_SILENT=4
FOF_ALLOWUNDO=64
FOF_NOCONFIRMATION=16

def recycle_path(path):
    path=os.path.normpath(path)
    s=Rs(None,FO_DELETE,path,None,FOF_SILENT|FOF_ALLOWUNDO|FOF_NOCONFIRMATION,None,None,None)
    p=byref(s)
    return Shlwapi.SHFileOperationW(p)

class Rs(Structure):
    _fields_ =[('hwnd',c_void_p),
               ('wFunc',c_uint),
               ('pFrom',c_wchar_p),
               ('pTo',c_wchar_p),
               ('fFlags',c_long),
               ('fAnyOperationsAborted',c_bool),
               ('hNameMappings',c_wchar_p),
               ('lpszProgressTitle',c_wchar_p)]
    

#print(Shlwapi.SHFileOperation)
#print(Shlwapi.shellcon)
if __name__=='__main__':
    print(recycle_path(u'D:/try/openssl\\goagent.cer'))