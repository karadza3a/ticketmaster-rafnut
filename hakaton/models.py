import json

from django.db import models
from rest_framework import serializers


class Customer(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    likes = models.CharField(max_length=2000)

    def set_likes(self, x):
        self.likes = json.dumps(x)

    def saved_likes(self):
        return json.loads(self.likes)


class CustomerSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200, read_only=True)
    saved_likes = serializers.CharField(required=False, allow_blank=True, max_length=2000)

    def create(self, validated_data):
        return Customer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.set_likes(validated_data.get('saved_likes', instance.saved_likes))
        instance.save()
        return instance
