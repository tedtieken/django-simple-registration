from django.conf import settings
from django.contrib.auth.models import User
 
class EmailBackend(object):
    def authenticate(self, email=None, username=None, password=None):
        if email:
            kwargs = {'email': email}
        elif username:
            if '@' in username:
                kwargs = {'email': username}
            else:
                return None
        else:
            return None
        
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
 
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class ForceBackend(object):
    def authenticate(self, username=None, password=None, force=False):
        if force == True and password == None:
            try:
                kwargs = {'username': username}
                return User.objects.get(**kwargs)
            except User.DoesNotExist:
                return None
        return None
    
    def get_user(self, user_id):
        try: 
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class EmailOrUsernameModelBackend(object):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
 
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None