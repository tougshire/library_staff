from django.views.generic.base import RedirectView
from django.urls import path, reverse_lazy
from . import views

app_name = "library_staff"

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("library_staff:position-list"))),
    path("position-list", views.PositionList.as_view(), name="position-list"),
]
