from django.urls import include, re_path
from taiga.urls import urlpatterns

urlpatterns += [
    re_path(r"^oidc/", include("mozilla_django_oidc.urls")),
]
