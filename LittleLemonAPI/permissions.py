from rest_framework import permissions 
from rest_framework.exceptions import PermissionDenied

class IsCustomer(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if view.__class__.__name__ == 'MenuItemListView' or view.__class__.__name__ == 'SingleMenuItemView':
            # Allow GET requests for authenticated users
            if request.method == 'GET' and request.user.is_authenticated and not request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
                return True
            # Denies all other requests for all authenticated users.
            else:
                return PermissionDenied('You do not have permission to perform this action.')
        #
        if view.__class__.__name__ == 'CartListCreateDestroyView':
            if request.method == ['GET', 'POST', 'DELETE'] and request.user.is_authenticated and not request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
                return True
            else:
                return False
            
        #
        if view.__class__.__name__ == 'OrderListCreateView':
            if request.method == ['GET', 'POST'] and request.user.is_authenticated and not request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
                return True
            else:
                return False
        #
        if view.__class__.__name__ == 'OrderDetailView':
            if request.method == ['GET', 'PUT', 'PATCH'] and request.user.is_authenticated and not request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
                return True
            else:
                return False
        
class IsDeliveryCrew(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if view.__class__.__name__ == 'MenuItemListView' or view.__class__.__name__ == 'SingleMenuItemView':
            # Allow GET calls for users who are members of the "delivery-crew" group
            if request.method == 'GET' and request.user.groups.filter(name='Delivery crew').exists():
                return True
            # Deny other requests for all delivery group members.
            else:
                return PermissionDenied('You do not have permission to perform this action.')
        #
        if view.__class__.__name__ == 'OrderListCreateView':
            if request.method == 'GET' and request.user.groups.filter(name='Delivery crew').exists():
                return True
            else:
                return False
        #
        if view.__class__.__name__ == 'OrderListCreateView':
            if request.method == 'GET' and request.user.groups.filter(name='Delivery crew').exists():
                return True
            else:
                return False
        #
        if view.__class__.__name__ == 'OrderDetailView':
            if request.method == 'PATCH' and request.user.groups.filter(name='Delivery crew').exists():
                return True
            else:
                return False
        
        
class IsManager(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if view.__class__.__name__ == 'MenuItemListView':
            # Allow GET and POST calls for users who are members of the "manager" group
            if request.method in ['GET', 'POST'] and request.user.groups.filter(name='Manager').exists():
                return True
            # Deny other requests for all manager group members.
            else:
                return PermissionDenied('You do not have permission to perform this action.')
        #
        if view.__class__.__name__ == 'SingleMenuItemView':
            if request.user.groups.filter(name='Manager').exists():
                return True
            else:
                return False
        #
        if view.__class__.__name__ == 'ManagerListCreateView':
            if request.user.groups.filter(name='Manager').exists():
                return True
            else: 
                return False 
        
        #
        if view.__class__.__name__ == 'OrderListCreateView':
            if request.method == 'GET' and request.user.groups.filter(name='Manager').exists():
                return True
            else:
                return False
        #
        if view.__class__.__name__ == 'OrderDetailView':
            if request.method == 'DELETE' and request.user.groups.filter(name='Manager').exists():
                return True
            else:
                return False
        