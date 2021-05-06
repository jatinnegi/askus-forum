from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):

        try:
            if '@' in username:
                user = User.objects.get(email=username)
            else:
                user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user

        return None
