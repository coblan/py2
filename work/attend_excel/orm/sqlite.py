

class Sqlite(object):
    @staticmethod
    def save(table, dc):
        querystr="INSERT INTO "+table.__name__+"("
        for k,v in dc.items():
            querystr+=k+","
        querystr=querystr.rstrip(",")
        querystr+=") VALUES ("
        for k,v in dc.items():
            querystr+= "%s"% table.getField(k).todb(v)+"," 
        querystr=querystr.rstrip(",")
        querystr+=")"
        return querystr
    
    @staticmethod
    def select(model,condition_str):
        querystr="SELECT "
        for k,v in model.fields:
            querystr+=k+','
        querystr=querystr.rstrip(",")
        querystr += " FROM %s %s"%( model.__name__,condition_str)
        return querystr
    
    @staticmethod
    def create(table):
        querystr = "CREATE TABLE "+table.__name__+"("
        for k,v in table.fields:
            querystr += v.createstr()+','
        querystr=querystr.rstrip(",")
        querystr+=")"
        return querystr
    @staticmethod
    def update(table,dc,autoId):
        querystr="UPDATE "+table.__name__+" SET "
        for k,v in dc.items():
            querystr+= k+"=%s"%table.getField(k).todb(v) +','
        querystr=querystr.rstrip(",")
        querystr+=" WHERE autoId=%s"%autoId
        return querystr