from rest_framework import serializers
import json

class UserSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'email': instance.email,
            'username': instance.username,
            'items': [x.id for x in instance.item_set.all()]
        }

class ItemSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'qrcode': instance.qrcode,
            'barcode': instance.barcode,
            'attrs': json.loads(instance.attrs),
            'tags': [x.tag for x in instance.tags.all()],
            'creatorId': instance.creator.id
        }

class ItemTemplateSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'attrs': json.loads(instance.attrs)
        }
