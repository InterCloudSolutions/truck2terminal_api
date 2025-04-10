from rest_framework import permissions, viewsets

from .models import Terminal
from .serializers import TerminalSerializer

# Create your views here.


class TerminalViewSet(viewsets.ModelViewSet):
    queryset = Terminal.objects.all()
    serializer_class = TerminalSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "slug"
