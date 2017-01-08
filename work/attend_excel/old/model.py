from orm import Model,Field

class RawRecord(Model):
    kao_number =Field()
    name = Field()
    department = Field()
    date = Field()
    workstart = Field()
    workleave = Field()
    
