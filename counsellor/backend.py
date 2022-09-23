from django.contrib.auth.backends import ModelBackend
from counsellor.models import Cousellor, User


class MultipleAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if kwargs.get('data_type') == 'counsellor':
            user_model = Cousellor
        else:
            user_model = User

        print(user_model.USERNAME_FIELD, username)
        print("password", password)

        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)

        if username is None or password is None:
            return
            
        try:
            user = user_model._default_manager.get_by_natural_key(username)
            print(user.is_staff)
        except user_model.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            user_model().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
