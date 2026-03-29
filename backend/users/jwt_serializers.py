from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from .serializers import UserSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user_data = UserSerializer(self.user).data
        user_data.pop("password", None)
        data['user'] = user_data
        data['token'] = data.pop('access')
        data.pop('refresh', None)
        return data