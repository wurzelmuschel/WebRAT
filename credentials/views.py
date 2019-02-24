from rest_framework import viewsets

from credentials.models import Credential
from credentials.serializers import CredentialSerializer


class CredentialViewSet(viewsets.ModelViewSet):
    """
    API endpoint
    """

    queryset = Credential.objects.all().order_by('-id')
    serializer_class = CredentialSerializer
