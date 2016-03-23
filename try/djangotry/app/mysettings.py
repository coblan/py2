import django
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#from django.conf import settings  
#settings.configure(  
    #DATABASES = {  
        #'default': {  
            #'ENGINE': 'django.db.backends.sqlite3',  
            #'NAME': r'd:/mydb.db3',  
            #'USER': '',  
            #'PASSWORD': '',  
            #'HOST': '',  
            #'PORT': '',  
        #}  
    #},
    #INSTALLED_APPS     = ( "app", )
#)  
#from django.conf import settings  
 
DATABASES = {  
    'default': {  
        'ENGINE': 'django.db.backends.sqlite3',  
        'NAME': r'd:/mydb.db3',  
        'USER': '',  
        'PASSWORD': '',  
        'HOST': '',  
        'PORT': '',  
    }  
}
#INSTALLED_APPS = ( "app", )

#django.setup()