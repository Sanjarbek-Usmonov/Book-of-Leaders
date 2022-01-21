from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import CustomUser


class UserSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = CustomUser.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'full_name', 'password',
                  'gender')

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_representation(self, ins):
        return {
            "id": ins.id,
            "username": ins.username,
            "full_name": ins.full_name,
            "gender": ins.gender
        }


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'full_name',
                   'gender')
        read_only_fields = ('password',)

    def to_representation(self, ins):
        return {
            "id": ins.id,
            "username": ins.username,
            "full_name": ins.full_name,
            "gender": ins.gender,
        }


# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
#         data.update({'id': self.user.id})
#         data.update({'username': self.user.username})
#         data.update({'full_name': self.user.full_name})
#         data.update({'gender': self.user.gender})
#
#         return data


class UpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('password', 'password2', 'old_password',)

    def validate(self, attrs):
        if len(attrs['password']) < 8:
            raise serializers.ValidationError(
                {"password": "Password length should not be less than 8 characters."})
        elif attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        attrs.pop('password2')
        attrs.pop('old_password')
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."})
        instance.set_password(validated_data['password'])
        instance.save()

        return instance

    def to_representation(self, ins):
        return {
            "detail": "your password has been changed"
        }