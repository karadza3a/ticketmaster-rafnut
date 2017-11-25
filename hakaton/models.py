import json

from django.db import models
from rest_framework import serializers


class Customer(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    likes = models.CharField(max_length=2000, blank=True)

    def set_likes(self, x):
        self.likes = json.dumps(x)

    def saved_likes(self):
        return json.loads(self.likes)


class CustomerSerializer(serializers.Serializer):
    id = serializers.CharField(max_length=200, read_only=True)
    saved_likes = serializers.CharField(required=False, allow_blank=True, max_length=2000)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class Plan(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer)
    plan_data = models.CharField(max_length=15000)


class PlanSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    id = serializers.IntegerField()
    plan_data = serializers.CharField()
