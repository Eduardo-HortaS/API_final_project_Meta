from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.MenuItemListView.as_view(), name='MenuItemListView'),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view(), name='SingleMenuItemView'),
    
    path('groups/manager/users', views.ManagerListCreateView.as_view(), name='ManagerListCreateView'),
    path('groups/manager/users/<int:pk>', views.ManagerDestroyView.as_view(), name='ManagerDestroyView'),
    path('groups/delivery-crew/users', views.DeliveryListCreateView.as_view(), name='DeliveryListCreateView'),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryDestroyView.as_view(), name='DeliveryDestroyView'),

    path('cart/menu-items', views.CartListCreateDestroyView.as_view(), name='CartListCreateDestroyView'),

    path('orders', views.OrderListCreateView.as_view(), name='OrderListCreateView'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='OrderDetailView'),
]
