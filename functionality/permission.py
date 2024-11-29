from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class HrOrAdmin(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.role in ['admin', 'hr']:
            raise PermissionDenied(detail='Only Admin Or Hr have permission to access')
        return True
    

class AdminOrHrOrPmOrTl(BasePermission):
    
    def has_permission(self, request, view):
        user = request.user
        if not user.role in ['admin', 'hr', 'pm', 'tl']:
            raise PermissionDenied(detail='Only Admin, Hr, Pm, Tl have permission to access')
        return True