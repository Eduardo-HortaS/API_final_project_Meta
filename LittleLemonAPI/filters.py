import django_filters
from .models import MenuItem, Order

class MenuItemFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    price = django_filters.NumberFilter()
    featured = django_filters.BooleanFilter()
    category = django_filters.CharFilter(field_name='category__title')
    
    class Meta:
        model = MenuItem
        fields = ['title', 'price', 'featured', 'category']
        
class OrderFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user__username')
    delivery_crew = django_filters.CharFilter(field_name='delivery_crew__username')
    status = django_filters.BooleanFilter()
    date = django_filters.DateFilter()
    min_total = django_filters.NumberFilter(field_name='total', lookup_expr='gte')
    max_total = django_filters.NumberFilter(field_name='total', lookup_expr='lte')
    
    class Meta:
        model = Order
        fields = ['user', 'delivery_crew', 'status', 'date', 'min_total', 'max_total']