from .models import CustomUser


class AuthenticationEmailBackend(object):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = CustomUser

        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if getattr(user, 'is_active', False) and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
