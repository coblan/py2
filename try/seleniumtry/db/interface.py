import os
import sys
#sys.path.append('.')
#sys.path.insert(0, '.')
#sys.path.append('../db')
base_dir = os.path.dirname(__file__)
sys.path.append(base_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'model.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from moon.models import TuiModel,Tag

def save_model(dc):
    url = dc.pop('url')
    t,c = TuiModel.objects.get_or_create(url=url)
    tag,c= Tag.objects.get_or_create(name=dc.pop('tag'))
    t.tag.add(tag)
    for k,v in dc.items():
        setattr(t,k,v)
    t.save()

#def save_email(email,title):
    #e,c =EmailModel.objects.get_or_create(email=email)
    #e.title=title
    #e.save()