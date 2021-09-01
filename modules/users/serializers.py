from datetime import datetime

from rest_framework import serializers
from modules.users.models import PanelUser


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    birthday = serializers.DateField()
    class Meta:
        model = PanelUser
        fields = ('username', 'email', 'first_name', 'is_active', 'gender', 'birthday', 'ranga', 'serwer', 'dzial', 'age')



