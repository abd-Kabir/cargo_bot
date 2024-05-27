from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.models import User
from apps.user.serializers.web import (PostUserSerializer, GetUserSerializer, PostCustomerSerializer,
                                       GetCustomerSerializer, RetrieveCustomerSerializer,
                                       PostResponseCustomerSerializer, PostResponseUserSerializer)
from config.core.api_exceptions import APIValidation
from config.core.pagination import APIPagination
from config.core.permissions.telegram import IsTGAdminOperator, IsTGOperator
from config.views import ModelViewSetPack


class UserModelViewSet(ModelViewSetPack):
    queryset = User.objects.filter(operator__isnull=False)
    serializer_class = GetUserSerializer
    permission_classes = [IsTGAdminOperator, ]
    post_serializer_class = PostUserSerializer
    pagination_class = APIPagination

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                response_serializer = PostResponseUserSerializer(instance=instance)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise APIValidation(f'Error occurred: {e.args[0]}', status_code=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PostResponseUserSerializer)
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            new_instance = self.get_object()
            response_serializer = PostResponseUserSerializer(instance=new_instance)
            response = response_serializer.data
            return Response(response)
        except Exception as e:
            raise APIValidation(f'Error occurred: {e.args[0]}', status_code=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PostUserSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class CustomerModelViewSet(ModelViewSetPack):
    queryset = User.objects.filter(customer__isnull=False)
    serializer_class = GetCustomerSerializer
    permission_classes = [IsTGOperator, ]
    post_serializer_class = PostCustomerSerializer
    pagination_class = APIPagination

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            return RetrieveCustomerSerializer(args[0])
        return super().get_serializer(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                response_serializer = PostResponseCustomerSerializer(instance=instance)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise APIValidation(f'Error occurred: {e.args[0]}', status_code=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PostCustomerSerializer)
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            new_instance = self.get_object()
            response_serializer = PostResponseCustomerSerializer(instance=new_instance)
            response = response_serializer.data
            return Response(response)
        except Exception as e:
            raise APIValidation(f'Error occurred: {e.args[0]}', status_code=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PostCustomerSerializer)
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class CustomerIDPrefix(APIView):
    """
    url-parameter choices: AVIA and AUTO
    """
    permission_classes = [IsTGOperator, ]

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