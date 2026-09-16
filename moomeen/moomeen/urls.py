from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path(
        "admin/",
        RedirectView.as_view(
            pattern_name="admin_dashboard",
            permanent=False,
        ),
    ),
    path("", include("store.urls")),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )