from django.urls import path
from django.views.decorators.http import require_POST
from profiles.views import (
    profile_detail_view,
    profile_redirect_view,
    profile_update_view,
)

app_name = "profiles"
urlpatterns = [
    path("~redirect/", view=profile_redirect_view, name="redirect"),
    path("~update/", view=profile_update_view, name="update"),
    path("<str:slug>/", view=profile_detail_view, name="detail"),
]