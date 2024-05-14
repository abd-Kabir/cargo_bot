from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.loads.filter import AdminProductFilter
from apps.loads.models import Product
from apps.loads.serializers.web import AdminProductListSerializer, AdminAddProductSerializer
from config.core.choices import PRODUCT_STATUS_CHOICE
from config.core.permissions.web import IsWebOperator


class AdminProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = AdminProductListSerializer
    permission_classes = [IsWebOperator, ]
    filterset_class = AdminProductFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, ]
    search_fields = ['barcode', 'customer__prefix', 'customer__code', 'accepted_by_china__full_name', ]

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(customer__prefix__startswith=search[:3]) | Q(customer__code__startswith=search[3:])
            )
        return queryset


class AdminSelectProductStatus(APIView):
    permission_classes = [IsWebOperator, ]

    @staticmethod
    def get(request, *args, **kwargs):
        response = []
        for product_status in PRODUCT_STATUS_CHOICE:
            if product_status[0] == 'NOT_LOADED':
                continue
            response.append({
                'value': product_status[0],
                'label': product_status[1],
            })
        return Response(response)


class AdminAddProduct(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = AdminAddProductSerializer
    permission_classes = [IsWebOperator, ]


class AdminUpdateProduct(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = AdminAddProductSerializer
    permission_classes = [IsWebOperator, ]
    http_method_names = ['patch', ]


class AdminDeleteProduct(DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsWebOperator, ]