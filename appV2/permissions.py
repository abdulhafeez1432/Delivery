from rest_framework import permissions



class IsLoggedInUserOrAdmin(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        return obj == request.user or request.user.is_staff


class IsAdminUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user and request.user.is_staff


class IsCustomerUser(permissions.BasePermission):

    def has_permission(self, request, view):
        #return request.user and request.user.is_customer
        return request.user

    def has_object_permission(self, request, view, obj):
        #return request.user and request.user.is_customer
        return request.user


class IsOwner(permissions.BasePermission):
        
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user