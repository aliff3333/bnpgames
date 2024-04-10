from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from bnpgames import settings

urlpatterns = [
    path('', include("apps.home.urls")),
    path('', include("apps.accounts.urls")),
    path('', include('allauth.urls')),
    path('cart/', include("apps.order.urls")),
    path('products/', include('apps.product.urls')),
    path('comments/', include('apps.comment.urls')),
    path('tinymce/', include('tinymce.urls')),
    path("__debug__/", include("debug_toolbar.urls")),
    path("admin/", admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
