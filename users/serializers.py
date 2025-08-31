from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

  def create(self, validated_data):
    user = User.objects.create_user(
      username=validated_data.get('username'),
      email=validated_data.get('email'),
      password=validated_data.get('password'),
      first_name=validated_data.get('first_name'),
      last_name=validated_data.get('last_name')
    )
    return user
  
class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'email', 'first_name', 'last_name')
    read_only_fields = ('id',)



class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email, 
            password=password
        )

        if not user:
            raise serializers.ValidationError(("Invalid email or password"))

        data = super().validate({
            "email": user.email,  
            "password": password,
        })

        data.update({
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
        })

        return data

