from datetime import datetime,tzinfo,timedelta

j = datetime.now()
k=datetime.utcnow()
class t(tzinfo):
    def utcoffset(self, datetime):
        return timedelta(hours=8)
    def dst(self, dt):
        # a fixed-offset class:  doesn't account for DST
        return timedelta(0)
    
class utc(tzinfo):
    def utcoffset(self, datetime):
        return timedelta(0)
    def dst(self, dt):
        # a fixed-offset class:  doesn't account for DST
        return timedelta(0)
    
print(j)
print(k)
kk = k.replace(tzinfo=utc())
print(kk)
f = kk.astimezone(t())
print(f)
print(f.time())