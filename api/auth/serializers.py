from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.auth.permissions import get_user_permissions


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        groups = user.groups.all()
        group_names = [group.name for group in groups]
        permissions = get_user_permissions(user)
        permission_names = [permission.codename for permission in permissions]

        token['permissions'] = permission_names
        token['roles'] = group_names
        token['username'] = user.username

        return token