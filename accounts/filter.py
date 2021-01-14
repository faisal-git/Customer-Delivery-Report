from django_filters import DateFilter, CharFilter,FilterSet
from .models import *

class orderFilter(FilterSet):
    dateFrom=DateFilter(field_name="date_created", lookup_expr='gte')
    dateTo=DateFilter(field_name="date_created", lookup_expr='gte')
    class Meta:
        model=Order
        fields='__all__'
        exclude=['customer','date_created']
