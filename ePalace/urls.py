from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/defualt/', admin.site.urls),

    path('accounts/', include('accounts.urls')),
    path('', include('user_panel.urls')),
    path('admin/', include('admin_panel.urls')),
] 
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



