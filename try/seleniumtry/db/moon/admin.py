from django.contrib import admin
from models import TuiModel

# Register your models here.

def field(header, **kwargs):
    def make_field(fun):
        for k, v in kwargs.iteritems():
            setattr(fun, k, v)
        fun.short_description = header
        return fun
    return make_field

class MamaTuiAdmin(admin.ModelAdmin):
    list_display=('url','price','title','get_img')
    
    @field('img',allow_tags=True)
    def get_img(self,obj):
        return '<img src={src} />'.format(src=obj.img)

admin.site.register(TuiModel,MamaTuiAdmin)
