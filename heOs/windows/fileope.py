#-*- encoding:utf8 -*-
from ctypes import *
from ctypes.wintypes import HWND,LPCWSTR,LPCSTR,LPWSTR,LPVOID,BOOL,DWORD

import os.path
Shell32=WinDLL('Shell32.dll')
FO_DELETE=3
FOF_SILENT=4
FOF_ALLOWUNDO=64
FOF_NOCONFIRMATION=16

def recycle_path(path):
    path=os.path.normpath(path)
    s=Rs(None,FO_DELETE,path,None,FOF_SILENT|FOF_ALLOWUNDO|FOF_NOCONFIRMATION,None,None,None)
    p=byref(s)
    return Shell32.SHFileOperationW(p)

class Rs(Structure):
    _fields_ =[('hwnd',c_void_p),
               ('wFunc',c_uint),
               ('pFrom',c_wchar_p),
               ('pTo',c_wchar_p),
               ('fFlags',c_long),
               ('fAnyOperationsAborted',c_bool),
               ('hNameMappings',c_wchar_p),
               ('lpszProgressTitle',c_wchar_p)]
    
Shell32.ShellExecuteW.argtypes=[HWND,LPCWSTR,LPCWSTR,LPCWSTR,LPCWSTR,c_int]

#Shell32=WinDLL('Shell32.dll')
def open_with_windows(path,arg=None):
    return Shell32.ShellExecuteW(None,'open',path,arg,None,3)


Kernel32=WinDLL('Kernel32.dll')
Kernel32.WinExec.argtypes=[LPCSTR,c_uint]
#Kernel32.CreateProcessW.argtypes=[LPCWSTR,LPWSTR,LPVOID,LPVOID,BOOL,DWORD,LPVOID,LPCWSTR,]
def open_with_create(path):
    return Kernel32.CreateProcessW('cmd.exe',' /c '+path,None,None,False,0x00000010,None,None,None,None)


if __name__=='__main__':
    #print(recycle_path(u'D:/try/openssl\\goagent.cer'))
    #print open_with_windows(r'cmd.exe',r'/c D:\coblan\py2\hetools\cmdgui\tmp.cmd')
    print(open_with_create(r'D:\coblan\py2\hetools\cmdgui\tmp.cmd'))