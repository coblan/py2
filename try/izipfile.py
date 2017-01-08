import zipfile
import os

idir = 'D:\coblan\py2\heQt'
with zipfile.ZipFile('trypkg.zip' ,'w') as izip:
    for r,ds,fs in os.walk(idir):
        for f in fs:
            filename=os.path.join(r,f)
            name=os.path.relpath(os.path.join(r,f),idir)
            izip.write( filename, name)
