from datetime import datetime

from rest_framework import serializers
from modules.users.models import PanelUser, UsersProfile


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    class Meta:
        model = PanelUser
        fields = ('username', 'email', 'first_name', 'is_active')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    birthday = serializers.DateField()

    class Meta:
        model = UsersProfile
        fields = ('user', 'gender', 'birthday', 'ranga', 'serwer', 'dzial', 'age')



