from models import Assortment, Configuration, PackageStyle
from rest_framework import serializers


class AssortmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assortment
        fields = ('id', 'choco_name', 'choco_config', 'choco_price', 'choco_pic', 'choco_dir', 'category', 'available', 'description')


class ConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configuration
        fields = ('id', 'size', 'weight', 'stock', 'diameter', 'height', 'weight', 'length')


class PackageStyleSerializer(serializers.ModelSerializer):

    class Meta:
        model = PackageStyle
        fields = ('id', 'package_name', 'package_pic')
