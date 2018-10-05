from models import Assortment, Configuration
from rest_framework import serializers


class AssortmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assortment
        fields = ('id', 'choco_name', 'choco_config', 'choco_price', 'choco_pic', 'choco_dir')


class ConfigurationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Configuration
        fields = ('id', 'choco_size', 'choco_weight', 'choco_quantity_in_box')
