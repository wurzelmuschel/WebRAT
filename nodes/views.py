from rest_framework import viewsets

from nodes.models import Node, Tag
from nodes.serializers import NodeSerializer, TagSerializer


class NodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint
    """

    queryset = Node.objects.all().order_by('-nodeid')
    serializer_class = NodeSerializer


class TagViewSet(viewsets.ModelViewSet):
    """

    """
    queryset = Tag.objects.all().order_by('-id')
    serializer_class = TagSerializer
