from django.contrib.auth.models import User, Group
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AccountSerializer(serializers.Serializer):
    acoount = serializers.IntegerField(primary_key=True, editable=True)
    name = serializers.CharField(max_length=30)
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.account = validated_data.get('account', instance.account)
        instance.name = validated_data.get('name', instance.name)
        instance.balance = validated_data.get('balance', instance.balance)
        instance.save()
        return instance