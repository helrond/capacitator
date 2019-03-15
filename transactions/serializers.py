from rest_framework import serializers
from .models import Container, Request, Pull, User


class ContainerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Container
        fields = '__all__'


class ContainerListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Container
        fields = ("url", "barcode", "size")


class RequestSerializer(serializers.HyperlinkedModelSerializer):
    containers = ContainerListSerializer(source='container_set', many=True)

    class Meta:
        model = Request
        fields = ("url", "total_space", "status", "end_time", "user", "containers")


class PullSerializer(serializers.HyperlinkedModelSerializer):
    containers = ContainerListSerializer(source='container_set', many=True)

    class Meta:
        model = Pull
        fields = ("url", "total_space", "status", "end_time", "containers")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("url", "username", "email", "is_superuser", "groups", "available_space")
