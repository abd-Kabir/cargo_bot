from django_filters import FilterSet, DateFilter

from apps.loads.models import Product


class AdminProductFilter(FilterSet):
    date = DateFilter(method='filter_date')

    @staticmethod
    def filter_date(queryset, name, value):
        return queryset.filter(updated_at__date=value)

    class Meta:
        model = Product
        fields = ['status',
                  'date', ]