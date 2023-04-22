from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404


class SnippetList(APIView):
    """"""
    def get(self, request, format=None):
        """"""
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """"""
        serializer = SnippetSerializer(data=request.data)
        # request.data can handle other other formats beyond json
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # returning response with data but allowing DRF to render into correct type
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)               


class SnippetDetail(APIView):
    """"""
    def get_object(self, pk):
        """"""
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """"""
        snippet = self.get_object(pk=pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """"""
        snippet = self.get_object(pk=pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        # request.data can handle other other formats beyond json
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            # returning response with data but allowing DRF to render into correct type
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """"""
        snippet = self.get_object(pk=pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)