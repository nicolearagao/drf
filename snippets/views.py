from rest_framework import generics
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from snippets.models import Snippet
from snippets.permissions import IsOwnerOrReadOnly
from snippets.serializers import SnippetSerializer, UserSerializer
from django.contrib.auth.models import User


class SnippetList(generics.ListCreateAPIView):
    """View for snippets list."""
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Map request's user to owner."""
        serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    """View for snippet detail."""
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class UserList(generics.ListAPIView):
    """View for users list."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """View for user detail."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["GET"])
def api_root(request, format=None):
    """View for api root url."""
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "snippets": reverse("snippet-list", request=request, format=format)
        }
        # using reverse function to return fully-qualified URLs
    )


class SnippetHighlight(generics.GenericAPIView):
    """View for snippets highlight."""
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]
    # pre-rendered HTML

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)
