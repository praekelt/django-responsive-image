from django.conf.urls import include, url

from layers.tests import views


urlpatterns = [
    url(
        r"^normal-view/$",
        views.NormalView.as_view(),
        name="normal-view"
    ),
    url(
        r"^web-only-view/$",
        views.WebOnlyView.as_view(),
        name="web-only-view"
    )
]
