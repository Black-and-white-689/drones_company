from django.contrib import admin

from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import static

from django.conf.urls import handler404, handler500

from django.shortcuts import render

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("drones.urls", namespace="drones")),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    def show_500(request):
        return render(request, "500.html", status=500)


    def show_404(request, exception=None):
        return render(request, "404.html", status=404)


    urlpatterns += [path("__debug__/", include(debug_toolbar.urls)),
                    path("test500/", show_500),
                    path("test404/", show_404), ]


def custom_404(request, exception):
    return render(request, "404.html", status=404)


def custom_500(request):
    return render(request, "500.html", status=500)


handler404 = "arms_drones.urls.custom_404"

handler500 = "arms_drones.urls.custom_500"
