from django.contrib import admin

from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import static

from django.shortcuts import render

from django.conf.urls import handler404, handler500


def demo_404(request):
    return render(request, "404.html", status=404)

def demo_500(request):
    return render(request, "500.html", status=500)


def custom_404(request, exception=None):
    return render(request, "404.html", status=404)

def custom_500(request):
    return render(request, "500.html", status=500)

handler404 = "arms_drones.urls.custom_404"

handler500 = "arms_drones.urls.custom_500"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("drones.urls", namespace="drones")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("demo404/", demo_404, name="demo_404"),
    path("demo500/", demo_500, name="demo_500"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("test500/", lambda r: render(r, "500.html", status=500)),
    ]
