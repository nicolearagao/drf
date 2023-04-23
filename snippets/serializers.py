from rest_framework import serializers
from snippets.models import Snippet
from django.contrib.auth.models import User

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for snippets objects."""
    owner = serializers.ReadOnlyField(source="owner.username")
    highlighted = serializers.HyperlinkedIdentityField(view_name="snippet-highlight", format="html")

    class Meta:
        model = Snippet
        fields = [
            "url", 'id', 'title', 'code', 'linenos', 'language', 'style', "owner", "highlighted",
            ]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for users."""
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name="snippet-detail", read_only=True)

    class Meta:
        model = User
        fields = ["url", "id", "username", "snippets"]
