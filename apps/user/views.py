from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.user.models import User
from apps.user.serializer import PostUserSerializer, GetUserSerializer, JWTLoginSerializer, PostCustomerSerializer, \
    GetCustomerSerializer, TelegramLoginSerializer, RetrieveCustomerSerializer
from apps.user.utils.services import authenticate_user, authenticate_telegram_user
from config.core.api_exceptions import APIValidation
from config.core.pagination import APIPagination
from config.core.permissions import IsOperator
from config.views import ModelViewSetPack


class JWTObtainPairView(TokenObtainPairView):
    serializer_class = JWTLoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response(authenticate_user(request))
        else:
            raise APIValidation(serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)


class TelegramLoginAPIView(APIView):
    serializer_class = TelegramLoginSerializer
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(request_body=TelegramLoginSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('tg_id'):
            return Response(authenticate_telegram_user(request, True))
        else:
            raise APIValidation('tg_id was not provided', status_code=status.HTTP_400_BAD_REQUEST)


class UserModelViewSet(ModelViewSetPack):
    queryset = User.objects.filter(operator__isnull=False)
    serializer_class = GetUserSerializer
    permission_classes = [IsOperator, ]
    post_serializer_class = PostUserSerializer
    pagination_class = APIPagination

    # def get_queryset(self):
    #     user = self.request.user
    #     queryset = super().get_queryset()
    #     if not user.is_superuser:
    #         queryset = queryset.filter(company_type=user.company_type).exclude(pk=user.id)
    #     return queryset

    @swagger_auto_schema(request_body=PostUserSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(request_body=PostUserSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class CustomerModelViewSet(ModelViewSetPack):
    queryset = User.objects.filter(customer__isnull=False)
    serializer_class = GetCustomerSerializer
    permission_classes = [IsOperator, ]
    post_serializer_class = PostCustomerSerializer
    pagination_class = APIPagination

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            return RetrieveCustomerSerializer(args[0])
        return super().get_serializer(*args, **kwargs)

    # def get_queryset(self):
    #     user = self.request.user
    #     queryset = super().get_queryset()
    #     if not user.is_superuser:
    #         queryset = queryset.filter(company_type=user.company_type)
    #     return queryset

    @swagger_auto_schema(request_body=PostCustomerSerializer)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(request_body=PostCustomerSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class CustomerIDPrefix(APIView):
    """
    url-parameter choices: AVIA and AUTO
    """
    permission_classes = [IsOperator, ]

    @staticmethod
    def get(request, *args, **kwargs):
        user_type = kwargs.get('user_type')
        if user_type == 'AUTO':
            response = [{'prefix': 'G'}, {'prefix': 'E'}, {'prefix': 'X'}, ]
        elif user_type == 'AVIA':
            response = [{'prefix': 'W'}, {'prefix': 'M'}, {'prefix': 'Z'}]
        else:
            raise APIValidation("Url parameter (user_type) accepts only AUTO or AVIA",
                                status_code=status.HTTP_400_BAD_REQUEST)
        return Response(response)
