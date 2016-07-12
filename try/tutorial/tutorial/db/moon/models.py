from django.db import models

# Create your models here.
class EmailModel(models.Model):
    email = models.CharField('email',max_length=400, blank=True)
    send = models.CharField('is send', max_length=100, blank=True)
    title = models.CharField('title', max_length=500, blank=True)
    check = models.CharField('check count', max_length=100, blank=True)
    
    #def save(self,*arg,**kw):
        #self.check = int(self.check) + 1
        #super(EmailModel,self).save(*arg,**kw)
        