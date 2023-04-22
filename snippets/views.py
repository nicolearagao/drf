from rest_framework import mixins
from rest_framework import generics
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetList(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
    """"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        """"""
        return self.list(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """"""
        return self.create(self, request, *args, **kwargs)


class SnippetDetail(generics.GenericAPIView, mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    """"""
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

    def get(self, request, *args, **kwargs):
        """"""
        self.retrieve(self, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """"""
        self.update(self, request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """"""
        self.destroy(self, request, *args, **kwargs)
