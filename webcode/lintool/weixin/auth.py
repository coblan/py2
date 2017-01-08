from django.contrib.auth.models import User
from lintool.struct import get_or_none

class MyBackend(object):
    """

    """

    def authenticate(self, token):
        if token == '778899':
            user = get_or_none(User,username='coblan')
            return user
        else:
            return None
            
            
        #login_valid = (settings.ADMIN_LOGIN == username)
        #pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        #if login_valid and pwd_valid:
            #try:
                #user = User.objects.get(username=username)
            #except User.DoesNotExist:
                ## Create a new user. Note that we can set password
                ## to anything, because it won't be checked; the password
                ## from settings.py will.
                #user = User(username=username, password='get from settings.py')
                #user.is_staff = True
                #user.is_superuser = True
                #user.save()
            #return user
        #return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None