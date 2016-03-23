#-*- coding: utf-8 -*-  


from django.db import models  
class MyModel(models.Model):  
    name = models.CharField(max_length = 50)  
    gender = models.BooleanField(default = False)  
    age = models.IntegerField(default = 0)  

    def __unicode__(self):  
        return self.name  

