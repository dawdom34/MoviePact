from rest_framework import serializers
from users.models import UserModel
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password



#Serializer to Register User
class RegisterSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
    validators=[UniqueValidator(queryset=UserModel.objects.all())]
  )
  password = serializers.CharField(
    write_only=True, required=True, validators=[validate_password])
  password2 = serializers.CharField(write_only=True, required=True)

  class Meta:
    model = UserModel
    fields = ('email', 'password', 'password2',)
    extra_kwargs = {
      'email': {'required': True}
    }

  # Password validation
  def validate(self, attrs):
    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    return attrs
  
  def create(self, validated_data):
    user = UserModel.objects.create(
      email=validated_data['email'],
    )
    user.set_password(validated_data['password'])
    user.save()
    return user


class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(
    required=True,
  )
  class Meta:
    model = UserModel
    fields = ('email', 'password')


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserModel
    fields = ('id', 'email')