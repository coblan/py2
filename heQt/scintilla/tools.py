import pickle
class ParseTool(object):
    def get(self,globeDict):
        self.mp={}
        for k ,v in globeDict.items():
            self.mp[k]=sorted( dir(v) )
        
    def save(self,path):

        with open(path,'wb') as f:
            pickle.dump(self.mp,f,2)
    
    
# 使用样例:
# 在需要解析的文件里面放入下面的东西
#obj = ParseTool()
#obj.get(globals())
#obj.save('dogbit')