from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import AllowList


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or 
            request.user and
            request.user.is_authenticated and
            request.user.is_staff,
        )
    

class AllowlistPermission(BasePermission): # Crud operation by using ip address.

    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        allowed = AllowList.objects.filter(ip_address=ip_addr).exists()
        return allowed
    

