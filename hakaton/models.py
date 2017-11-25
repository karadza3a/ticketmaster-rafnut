import json

from django.db import models
from rest_framework import serializers


class Customer(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    likes = models.CharField(max_length=2000, blank=True)

    def set_likes(self, x):
        self.likes = json.dumps(x)

    def saved_likes(self):
        if len(self.likes) > 0:
            return json.loads(self.likes)
        else:
            return []


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


class FlightPriceCache(models.Model):
    id = models.AutoField(primary_key=True)
    start_lat = models.FloatField()
    start_lng = models.FloatField()
    end_lat = models.FloatField()
    end_lng = models.FloatField()
    price = models.FloatField()

    def __str__(self):
        return "FPC price: %f" % self.price


class HotelPriceCache(models.Model):
    id = models.AutoField(primary_key=True)
    lat = models.FloatField()
    lng = models.FloatField()
    price = models.FloatField()


class HotelCache(models.Model):
    id = models.AutoField(primary_key=True)
    lat = models.FloatField()
    lng = models.FloatField()
    json_value = models.CharField(max_length=200000)
