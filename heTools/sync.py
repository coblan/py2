from heOs.syndir import SynCopy,SynDel
import sys
import argparse
from peewee import *
from os.path import getmtime
import os.path
parser = argparse.ArgumentParser() 
parser.add_argument("f", help="echo the string you use here") 
args = parser.parse_args()


if args.f:
    execfile(args.f)

db = SqliteDatabase('sync.db')

class MTimes(Model):
    name = CharField(unique=True)
    mtime=IntegerField(default=0)

    class Meta:
        database = db # This model uses the "people.db" database.
db.connect()

#db.create_tables([MTimes])


class CustomSync(SynCopy):
    #def __init__(self,src,dst):
        #super(CustomSync,self).__init__(src,dst)
        #self.success_update.connect(self.write_to_db)
        
    def should_incude_name(self,src,dst):
        if src.endswith(ignore_files):
            return False
        elif not os.path.exists(dst):
            return True
        elif int(getmtime(src))>int(getmtime(dst)):
            return True
        #else:
            #if not os.path.exists(dst):
                #tm,c=MTimes.get_or_create(name=dst)
                #dst_mtime=tm.mtime
            #else:
                #dst_mtime=int(getmtime(dst))
            #if int(getmtime(src))>dst_mtime:
                #return True
  
    def write_to_db(self,src,dst):
        tm=int(getmtime(dst))
        f,c=MTimes.get_or_create(name=dst)        
        f.mtime=tm
        f.save()
    
    
for src,dst in dirs:
    s=CustomSync(src,dst)
    s.run()
    s=CustomSync(dst,src)
    s.run()
    #s=SynDel(src,dst)
    #s.run()
    #s=SynDel(dst,src)
    #s.run()
    #syn_copy(src, dst,ignore_dir,ignore_file)
    #syn_copy(dst,src,ignore_dir,ignore_file)