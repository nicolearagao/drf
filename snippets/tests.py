import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from snippets.views import SnippetList, SnippetDetail, UserList, UserDetail, api_root, SnippetHighlight
from snippets.models import Snippet


factory = APIRequestFactory()

@pytest.fixture
@pytest.mark.django_db
def user():
    """Return user instance."""
    user = User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpass"
    )
    return user


@pytest.fixture
@pytest.mark.django_db
def snippet(user):
    """Return snippet instance."""
    snippet = Snippet.objects.create(code="print('Hello, Nicole!')", owner=user)
    return snippet

@pytest.mark.django_db
def test_snippet_list():
    """Test getting a list of snippets."""
    url = reverse("snippet-list")
    request = factory.get(url)
    response = SnippetList.as_view()(request)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_snippet_create_no_auth():
    """Test creating a snippet without auth."""
    url = reverse("snippet-list")
    data = {"code": "print('Hello, Nicole!')"}
    request = factory.post(url, data=data)
    response = SnippetList.as_view()(request)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_snippet_create_with_auth(user):
    """Test creating a snippet without auth."""
    url = reverse("snippet-list")
    data = {"code": "print('Hello, Nicole!')"}
    request = factory.post(url, data=data)
    force_authenticate(request, user=user)
    response = SnippetList.as_view()(request)
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == ""
    assert response.data["code"] == data["code"]


@pytest.mark.django_db
def test_snippet_detail(snippet):
    """Test getting a single snippet."""
    url = reverse("snippet-detail", args=[snippet.id])
    request = factory.get(url)
    response = SnippetDetail.as_view()(request, pk=snippet.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == snippet.id


@pytest.mark.django_db
def test_snippet_update_with_auth(snippet, user):
    """Test updating a snippet."""
    url = reverse("snippet-detail", args=[snippet.id])
    assert snippet.title == ""

    data = {"title": "Updated Snippet", "code": snippet.code}
    request = factory.put(url, data)
    force_authenticate(request, user=user)
    response = SnippetDetail.as_view()(request, pk=snippet.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == data["title"]


@pytest.mark.django_db
def test_snippet_delete(snippet, user):
    """Test deleting a snippet."""
    url = reverse("snippet-detail", args=[snippet.id])
    request = factory.delete(url)
    force_authenticate(request, user=user)
    response = SnippetDetail.as_view()(request, pk=snippet.id)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_list():
    """Test getting list of users."""
    url = reverse("user-list")
    request = factory.get(url)
    response = UserList.as_view()(request)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_detail(user):
    """Test getting s single user."""
    url = reverse("user-detail", args=[user.id])
    request = factory.get(url)
    force_authenticate(request, user=user)
    response = UserDetail.as_view()(request, pk=user.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == user.id


@pytest.mark.django_db
def test_api_root():
    """Testing api root."""
    url = "/"
    request = factory.get(url)
    response = api_root(request)

    assert response.status_code == status.HTTP_200_OK
    assert "users" in response.data
    assert "snippets" in response.data


@pytest.mark.django_db
def test_snippet_highlight(snippet):
    """Test getting the highlighted code for a snippet."""
    url = reverse("snippet-highlight", args=[snippet.id])
    request = factory.get(url)
    response = SnippetHighlight.as_view()(request, pk=snippet.id)
    response.render()

    assert response.status_code == status.HTTP_200_OK
    assert snippet.highlighted.encode("utf-8") in response.content
