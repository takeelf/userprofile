from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import NotFound

from basic_account.models import UserProfile


class UserSerializer(serializers.ModelSerializer):
    real_name = serializers.CharField(source='profile.real_name', required=True)
    is_authentication = serializers.BooleanField(source='profile.is_authentication', required=False)
    thumbnail_file = serializers.ImageField(source='profile.thumbnail_file', allow_null=True, required=False)

    class Meta:
        model = User

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        validated_data.pop('groups')
        validated_data.pop('user_permissions')
        user = User.objects.create(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user

    @transaction.atomic
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        if profile_data is not None:
            try:
                profile = UserProfile.objects.get(user=instance)
                super(UserSerializer, self).update(profile, profile_data)
            except UserProfile.DoesNotExist:
                raise NotFound
        user = super(UserSerializer, self).update(instance, validated_data)
        return user
