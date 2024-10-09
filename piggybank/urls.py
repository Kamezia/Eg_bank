from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("core.urls")),
    path("login/", obtain_auth_token), # Create the token when you enter username and password
    path('api-auth/', include('rest_framework.urls')),
]
