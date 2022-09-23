from django.contrib.auth.backends import ModelBackend
from counsellor.models import Counsellor, User


class MultipleAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(kwargs)
        if kwargs.get('data_type') == 'counsellor':
            user_model = Counsellor
        else:
            user_model = User
        print("Model", user_model)
        if username is None:
            username = kwargs.get(user_model.USERNAME_FIELD)
        print("Username", username)
        if username is None or password is None:
            return
            
        try:
            user = user_model._default_manager.get_by_natural_key(username)
            print("User",user)
            
        except (user_model.DoesNotExist, AttributeError):
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            user_model().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
