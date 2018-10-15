from models import Assortment, Configuration
from rest_framework import serializers


class AssortmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assortment
        fields = ('id', 'choco_name', 'choco_config', 'choco_price', 'choco_pic', 'choco_dir', 'category', 'available', 'description')


class ConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configuration
        fields = ('id', 'size', 'weight', 'quantity', 'diameter', 'height', 'weight', 'length')
