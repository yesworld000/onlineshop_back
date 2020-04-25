# from django_filters import rest_framework as filters
#
# from api.models import Product
#
#
# class ProductFilter(filters.FilterSet):
#     name = filters.CharFilter(lookup_expr='contains')
#     min = filters.NumberFilter(field_name='price', lookup_expr='gte')
#     max = filters.NumberFilter(field_name='price', lookup_expr='lte')
#
#     class Meta:
#         model = Product
#         fields = ('name', 'min', 'max')
