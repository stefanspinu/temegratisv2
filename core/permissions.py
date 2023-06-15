from rest_framework import permissions
from .models import AcceptedOrder

class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.user == request.user


class IsClientOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return request.user.groups.filter(name='clients').exists()


class IsOwnerOrReadOnlyClient(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.client.user


from rest_framework import permissions

# class IsFreelancerOrClientWithPaidFalse(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         if request.user.groups.filter(name='freelancer').exists() and obj.paied==False:
#             return True
#         elif request.user.groups.filter(name='client').exists() and obj.paied==True:
#             return True
