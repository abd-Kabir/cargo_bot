from django.urls import path

from apps.loads.routes.telegram import BarcodeConnectionAPIView, AcceptProductAPIView, OperatorStatisticsAPIView, \
    LoadInfoAPIView, AddLoadAPIView, ModerationNotProcessedLoadAPIView, ModerationProcessedLoadAPIView, \
    CustomerOwnLoadsHistoryAPIView, CustomerCurrentLoadAPIView, ModerationLoadPaymentAPIView, \
    ModerationLoadApplyAPIView, ModerationLoadDeclineAPIView, ReleaseLoadInfoAPIView, ReleasePaymentLoadAPIView, \
    ReleaseLoadAPIView, CustomerTrackProductAPIView, CustomerProductsListAPIView
from apps.loads.routes.web import AdminProductListAPIView, AdminSelectProductStatus, AdminAddProduct, \
    AdminUpdateProduct, AdminDeleteProduct, AdminLoadListAPIView, AdminLoadRetrieveAPIView, AdminLoadUpdateAPIView
from apps.loads.views import OpenProductBarcodeAPIView

app_name = 'api'
urlpatterns = [
    # admin
    path('open/product/<str:barcode>/', OpenProductBarcodeAPIView.as_view(), name='open_product_barcode'),

    path('admin/delivery/products/', AdminProductListAPIView.as_view(), name='admin_delivery_products'),
    path('admin/delivery/product-statuses/', AdminSelectProductStatus.as_view(), name='admin_select_status'),
    path('admin/delivery/product-add/', AdminAddProduct.as_view(), name='admin_add_product'),
    path('admin/delivery/product-update/<int:pk>/', AdminUpdateProduct.as_view(), name='admin_update_product'),
    path('admin/delivery/product-delete/<int:pk>/', AdminDeleteProduct.as_view(), name='admin_delete_product'),
    path('admin/loads/list/', AdminLoadListAPIView.as_view(), name='admin_loads_list'),
    path('admin/loads/retrieve/<int:pk>/', AdminLoadRetrieveAPIView.as_view(), name='admin_loads_retrieve'),
    path('admin/loads/update/<int:pk>/', AdminLoadUpdateAPIView.as_view(), name='admin_loads_update'),

    # bot-operator
    path('operator/china/barcode-connection/', BarcodeConnectionAPIView.as_view(), name='china_barcode'),
    path('operator/tashkent/accept-product/<str:barcode>/', AcceptProductAPIView.as_view(), name='tashkent_accept'),
    path('operator/daily-stats/', OperatorStatisticsAPIView.as_view(), name='operator_daily_stats'),

    path('operator/tashkent/load-info/', LoadInfoAPIView.as_view(), name='tashkent_load_info'),
    path('operator/tashkent/add-load/', AddLoadAPIView.as_view(), name='tashkent_add_load'),

    path('operator/tashkent/release/load-info/<str:customer_id>/',
         ReleaseLoadInfoAPIView.as_view(), name='tashkent_release_load_info'),
    path('operator/tashkent/release/payment/<str:customer_id>/',
         ReleasePaymentLoadAPIView.as_view(), name='tashkent_release_payment'),
    path('operator/tashkent/release/<str:customer_id>/', ReleaseLoadAPIView.as_view(), name='tashkent_release'),

    path('operator/tashkent/moderation/applications/not-processed/',
         ModerationNotProcessedLoadAPIView.as_view(), name='tashkent_applications_not_processed'),
    path('operator/tashkent/moderation/applications/processed/',
         ModerationProcessedLoadAPIView.as_view(), name='tashkent_applications_processed'),
    path('operator/tashkent/moderation/get-application/<str:application_id>/',
         ModerationLoadPaymentAPIView.as_view(), name='tashkent_application_retrieve'),
    path('operator/tashkent/moderation/apply-application/<str:application_id>/',
         ModerationLoadApplyAPIView.as_view(), name='tashkent_application_apply'),
    path('operator/tashkent/moderation/decline-application/<str:application_id>/',
         ModerationLoadDeclineAPIView.as_view(), name='tashkent_application_decline'),

    # bot-customer
    path('customer/current-load/', CustomerCurrentLoadAPIView.as_view(), name='customer_own_loads'),
    path('customer/own-loads/history/', CustomerOwnLoadsHistoryAPIView.as_view(), name='customer_own_loads'),
    path('customer/track/product/<str:barcode>/', CustomerTrackProductAPIView.as_view(), name='customer_track_product'),
    path('customer/products-on-way/list/', CustomerProductsListAPIView.as_view(), name='customer_products_on_way_list'),

    # common
]
