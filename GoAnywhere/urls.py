from django.contrib import admin
from django.urls import path, include
# hjsdf
urlpatterns = [
    path ('', include('home.urls')),
    path ('account/', include('account.urls')),
    path('admin/', admin.site.urls),
]
