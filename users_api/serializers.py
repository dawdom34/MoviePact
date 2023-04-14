from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import UserModel

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode



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


# Serializer to login user
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


# Serializer to change password
class UserChangePasswordSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    password = attrs.get('password')
    password2 = attrs.get('password2')
    user = self.context.get('user')
    # Check if password match
    if password != password2:
      raise serializers.ValidationError(
        {"password": "Password fields didn't match."})
    # Set new password
    user.set_password(password)
    user.save()
    return attrs
  

# Serializer to send reset password email
class SendPasswordResetEmailSerializer(serializers.Serializer):
  email = serializers.EmailField(max_length=255)

  class Meta:
    fields = ['email']

  def validate(self, attrs):
    email = attrs.get('email')
    # Check if user with given email exist
    if UserModel.objects.filter(email=email).exists():
      # Get user from db
      user = UserModel.objects.get(email=email)
      # Encode user id 
      uid = urlsafe_base64_encode(force_bytes(user.id))
      print('Encoded uid', uid)
      # Generate token
      token = PasswordResetTokenGenerator().make_token(user)
      print('Password reset token generated', token)
      # Generate password reset link
      link = 'http://localhost:8000/users_api/reset-password/' + uid + '/' + token
      print('Password reset link', link)
      return attrs
    else:
      raise serializers.ValidationError('You are not registered user')
    

# Serializer to reset user password
class PasswordResetSerializer(serializers.Serializer):
  password = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)
  password2 = serializers.CharField(max_length=255, style={'input_type': 'password'}, write_only=True)

  class Meta:
    fields = ['password', 'password2']

  def validate(self, attrs):
    
    password = attrs.get('password')
    password2 = attrs.get('password2')
    uid = self.context.get('uid')
    token = self.context.get('token')
    try:
      # Check if passwords match
      if password != password2:
        raise serializers.ValidationError(
          {"password": "Password fields didn't match."})
      # Decode user id 
      id = smart_str(urlsafe_base64_decode(uid))
      # Get user from db
      user = UserModel.objects.get(id=id)
      # Check if token is valid
      if not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not valid or expired')
      # Set new password
      user.set_password(password)
      user.save()
      return attrs
    except DjangoUnicodeDecodeError:
      if  not PasswordResetTokenGenerator().check_token(user, token):
        raise serializers.ValidationError('Token is not valid or expired')