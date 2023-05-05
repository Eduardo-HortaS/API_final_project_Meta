
from django.contrib.auth.models import User, Group
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
from django.core.paginator import Paginator, EmptyPage
from django_filters.rest_framework import DjangoFilterBackend 
from .filters import MenuItemFilter, OrderFilter

from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import GroupSerializer, UserSerializer, MenuItemSerializer, CategorySerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from .permissions import IsCustomer, IsDeliveryCrew, IsManager



class MenuItemListView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsCustomer, IsDeliveryCrew, IsManager]
    filterset_class = MenuItemFilter
    ordering_fields = ['title','price']
        
    def get_permissions(self):
        # Allows customers and delivery crew to make GET requests only, but managers can make GET and POST.
        return [permission() for permission in self.permission_classes]

            
            
class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsCustomer, IsDeliveryCrew, IsManager]

    def get_permissions(self):
        # Allows customers and delivery crew to make GET requests only, but managers can make GET, PUT, PATHC and DELETE calls
        return[permission() for permission in self.permission_classes]
    
class ManagerListCreateView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name = 'Manager')
    serializer_class = UserSerializer
    permission_classes = [IsManager]
    group_name = 'Manager'
    
    def create(self, request, *args, **kwargs):
        try:
            username_of_interest = request.data.get('username')
            user = User.objects.get(username=username_of_interest)
            group = Group.objects.get(name=self.group_name)
            group.user_set.add(user)
            group.save()
            return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)
        
class ManagerDestroyView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name = 'Manager')
    serializer_class = UserSerializer
    permission_classes = [IsManager]
    group_name = 'Manager'

    def delete(self, request, *args, **kwargs):
        try:
            user_id = int(request.data.get('id'))
            user = User.objects.get(pk=user_id)
            group = Group.objects.get(name=self.group_name)
            group.user_set.remove(user)
            group.save()
            return Response({'message': 'user removed from the group'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)

class DeliveryListCreateView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name = 'Delivery crew')
    serializer_class = UserSerializer
    permission_classes = [IsManager]
    group_name = 'Delivery crew'
    
    def create(self, request, *args, **kwargs):
        try:
            user_id = int(request.data.get('id'))
            user = User.objects.get(pk=user_id)
            group = Group.objects.get(name=self.group_name)
            group.user_set.add(user)
            group.save()
            return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response({'id': 'a valid integer is required'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)

class DeliveryDestroyView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = User.objects.filter(groups__name = 'Delivery crew')
    serializer_class = UserSerializer
    permission_classes = [IsManager]
    group_name = 'Delivery crew'

    def delete(self, request, *args, **kwargs):
        try:
            user_id = int(request.data.get('id'))
            user = User.objects.get(pk=user_id)
            group = Group.objects.get(name=self.group_name)
            group.user_set.remove(user)
            group.save()
            return Response({'message': 'user removed from the group'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)

class CartListCreateDestroyView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    model = Cart
    queryset = model.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCustomer]
    related_model = MenuItem

    def get_queryset(self):
        # Filter Cart object by the current user, a user can only have one cart?
        user = self.request.user
        user_cart_item = self.model.objects.filter(user=user)
        if user_cart_item:
            # Get the associated MenuItem objects
            menu_items = [Cart.menuitem for Cart in user_cart_item]
            return menu_items
        else:
            # Create a new Cart object associated with that user if it doesn't exist
            cart_object = self.model.objects.create(user=user)
            cart_object.save()
            return cart_object

    def perform_create(self, serializer):
        # Set the user field on the cart item to the current user
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Get the menu item id from the request data
        menu_item_id = self.request.data.get('menuitem_id')
        # Get the user from the authenticated user
        user = self.request.user
        # Get the quantity from the request data
        quantity = self.request.data.get('quantity')
        # Calculate the unit price and total price
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        unit_price = menu_item.price
        price = unit_price * quantity
        
        # Create the cart item
        cart_item = Cart.objects.create(
            user=user,
            menuitem=menu_item,
            quantity=quantity,
            unit_price=unit_price,
            price=price
        )

        serializer = self.serializer_class(cart_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def delete(self, request, *args, **kwargs):
        # Get the authenticated user id
        user_id = self.request.user.id
        # Delete all cart items created by the authenticated user id
        Cart.objects.filter(user_id=user_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderListCreateView(generics.ListCreateAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter
    search_fields = ['user__username', 'delivery_crew__username']
    permission_classes = [IsCustomer, IsManager, IsDeliveryCrew]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            # Code for managers
            queryset = Order.objects.all().prefetch_related('orderitems') 
        if user.groups.filter(name='Delivery crew').exists():
            # Code for delivery crew
            queryset = Order.objects.filter(delivery_crew=user).prefetch_related('orderitems')
        else:
            # Code for Customers
            queryset = Order.objects.filter(user=user).prefetch_related('orderitems')
        return queryset
    

    def perform_create(self, serializer):
        # This code should only execute for customers
        if not self.request.user.groups.filter(name__in=['Manager', 'Delivery crew']).exists():
            # Get the current user
            user = self.request.user
            # Create a new order with the user
            order = serializer.save(user=user)
            # Get the cart items for the user
            cart_items = Cart.objects.filter(user=user)
            # Create order items from cart items and associate them with the new order
            order_items = []
            for cart_item in cart_items:
                order_item = OrderItem(
                    order=order,
                    menuitem=cart_item.menuitem,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.unit_price,
                    price=cart_item.price,
                )
                order_items.append(order_item)
            # Bulk create the order items
            OrderItem.objects.bulk_create(order_items)
            # Delete all items from the cart for this user
            Cart.objects.filter(user=user).delete()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    model = Order
    queryset = model.objects.all()
    serializer_class = OrderSerializer
    ordering_fields = ['user', 'delivery_crew', 'status', 'date']
    search_fields = ['user', 'delivery_crew', 'status', 'date']
    filterset_fields = ['user', 'delivery_crew', 'status', 'date'] 
    permission_classes = [IsCustomer, IsManager, IsDeliveryCrew]  
    
    def get_object(self):
        # Get the order instance
        order_id = self.kwargs.get('pk')
        order = get_object_or_404(Order, id=order_id)
        # Check if the order belongs to the current user
        if order.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this order.")
        return order
    
    def get(self, request, *args, **kwargs):
        # Get the order instance using the overridden get_object method
        order = self.get_object()
        
        # Get all the order items related to the order instance
        order_items = order.orderitems.all()
        
        # Serialize the order and order items
        order_serializer = OrderSerializer(order)
        order_items_serializer = OrderItemSerializer(order_items, many=True)
        data = {
            'order': order_serializer.data,
            'order_items': order_items_serializer.data
        }
        
        return Response(data)
    
    def update(self, request, *args, **kwargs):
        # Get the order instance using the overridden get_object method
        order = self.get_object() 
        # Check if the current user is a Manager
        if request.user.groups.filter(name='Manager').exists():
            # Check if the request includes a delivery crew member ID
            delivery_crew_id = request.data.get('delivery_crew')
            if delivery_crew_id:
                # Get the delivery crew member instance
                delivery_crew = get_object_or_404(User, id=delivery_crew_id)
                # Set the delivery crew member for the order
                order.delivery_crew = delivery_crew
                order.save()

            # Check if the request includes an updated status
            status = request.data.get('status')
            if status is not None:
                # Set the updated status for the order
                order.status = bool(status)
                order.save()
        # Check if the current user is instead the delivery crew member assigned to the order    
        elif request.user == order.delivery_crew:
            # Check if the request includes an updated status
            status = request.data.get('status')
            if status is not None:
                # Set the updated status for the order
                order.status = bool(status)
                order.save(update_fields=['status'])
        else:
            raise PermissionDenied("You do not have permission to update this order.")
        
        # Get all order items related to the order instance
        order_items = order.orderitems.all()
        
        # Serialize the updated order and order items
        order_serializer = OrderSerializer(order)
        order_items_serializer = OrderItemSerializer(order_items, many=True)
        data = {
            'order': order_serializer.data,
            'order_items': order_items_serializer.data
        }
        return Response(data)
        
    
    def delete(self, request, *args, **kwargs):
        # Check if the current user is a Manager
        if not request.user.groups.filter(name='Manager').exists():
            raise PermissionDenied("You do not have permission to delete this order.")
        # Get the order instance using the overridden get_object method
        order = self.get_object()
        # Delete the order instance
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)