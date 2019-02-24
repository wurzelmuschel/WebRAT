from rest_framework import serializers

from credentials.models import Credential


class CredentialSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField()
    passphrase = serializers.CharField()
    key = serializers.CharField()

    class Meta:
        model = Credential
        fields = ('name',
                  'notes',
                  'tags',
                  # 'username',
                  'password',
                  'passphrase',
                  'key',
                  'owner',
                  )
