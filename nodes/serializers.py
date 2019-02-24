from rest_framework import serializers

from nodes.models import Node, Tag


class NodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Node
        fields = ('nodeid',
                  'hostname',
                  'site_code',
                  # 'owners',
                  'notes',
                  'tags',
                  'last_edit',
                  # 'last_editor,
                  'autoupdate_enabled',
                  'autoupdate_branch',
                  'firmware_base',
                  'firmware_release',
                  'model',
                  'last_import',
                  'first_import',
                  'last_seen',
                  'is_online',
                  'longitude',
                  'latitude',
                  'gateway',
                  'gateway_nexthop',
                  'ipaddress',
                  'credentials',
                  )


class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
