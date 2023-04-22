from django.urls import path
from snippets import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("snippets/", views.snippet_list),
    path("snippets/<int:pk>/", views.snippet_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
# adding this to urls to make sure the api will be able to handle URLs that
# explicitly refer to a given format
