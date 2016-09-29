from django.db import models

# Create your models here.

class Tag(models.Model):
    name= models.CharField('name', max_length=100,blank=True)

class TuiModel(models.Model):
    url = models.CharField('url', max_length=700,blank=True)
    img = models.CharField('img', max_length=700,blank=True)
    title = models.CharField('title', max_length=700,blank=True)
    price = models.CharField('price', max_length=100,blank=True)
    #tag = models.CharField('tag', max_length=700,blank=True)
    tag = models.ManyToManyField(Tag,null=True,blank=True)
    update_at = models.DateTimeField(verbose_name='update time',auto_now=True,blank=True,null=True)
    lukou = models.CharField('send to lulou', max_length=100,blank=True,default='no')
    

