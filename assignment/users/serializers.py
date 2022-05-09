from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import User_Profile


class UserSerializers(serializers.ModelSerializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    user_role = serializers.CharField(required=True)

    class Meta:
        model = User_Profile
        fields = ('email', 'password', 'first_name', 'last_name', 'user_role')

    def create(self, validated_data):
        # 1. User request with email and  password, role, first name and last name
        user, created = User.objects.get_or_create(username=validated_data.get('email').lower(),
                                                   first_name=validated_data.get('first_name'),
                                                   last_name=validated_data.get('last_name'),
                                                   email=validated_data.get('email').lower())
        user.set_password(validated_data.get('password'))
        user.save()
        if created:
            userprofile = User_Profile(user_role=validated_data.get('user_role'), user=user)
            userprofile.save()
        return validated_data

class UserProfileSerializers(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='user.email')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')

    class Meta:
        model = User_Profile
        fields = ('email', 'first_name', 'last_name', 'user_role')


