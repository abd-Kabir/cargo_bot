from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from apps.user.models import Customer
from config.core.api_exceptions import APIValidation


def start_prefix(user_type):
    if user_type == 'AUTO':
        return 'WSC'
    elif user_type == 'AVIA':
        return 'HVP'
    else:
        raise APIValidation('user_type must be AUTO or AVIA')


def next_prefix(last_prefix, user_type):
    if user_type == 'AUTO':
        if last_prefix == 'WSC':
            return 'YDQ'
        return 'ZRD'
    elif user_type == 'AVIA':
        if last_prefix == 'HVP':
            return 'LXE'
        return 'GZG'
    else:
        raise APIValidation('user_type must be AUTO or AVIA')


def generate_code(customer_data: dict) -> tuple:
    user_type = customer_data.get('user_type')
    query = Customer.objects.filter(user_type=user_type, prefix__isnull=False, code__isnull=False).order_by('id')
    if query.exists():
        last_prefix = query.last().prefix
    else:
        last_prefix = start_prefix(user_type)

    customers_with_last_prefix = query.filter(prefix=last_prefix).order_by('code')
    codes = [int(c.code) for c in customers_with_last_prefix]
    max_code = max(codes) if codes else 0
    next_code = None
    for i in range(1, max_code + 2):
        if i not in codes:
            next_code = str(i).zfill(4)
            break

    customers_count = query.filter(prefix=last_prefix).count()
    if customers_count > 3000:
        prefix = last_prefix
        code = next_code if next_code else str(customers_count).zfill(4)
        return prefix, code
    elif customers_count == 3000 and last_prefix not in ['ZRD', 'GZG']:
        prefix = next_code if next_code else next_prefix(last_prefix, user_type)
        code = str(1).zfill(4)
        return prefix, code

    prefix = last_prefix
    code = next_code if next_code else str(customers_count + 1).zfill(4)
    return prefix, code


def prefix_check(prefix, user_type):
    if not prefix and not user_type:
        raise APIValidation('Prefix, user_type was not provided', status_code=status.HTTP_400_BAD_REQUEST)
    if prefix in ['WSC', 'YDQ', 'ZRD'] and user_type == 'AUTO':
        return True
    elif prefix in ['HVP', 'LXE', 'GZG'] and user_type == 'AVIA':
        return True
    else:
        raise APIValidation("Wrong combination of prefix and user_type",
                            status_code=status.HTTP_400_BAD_REQUEST)


def authenticate_user(request, is_telegram: bool = False):
    user = authenticate(request,
                        username=request.data['username'],
                        password=request.data['password'],
                        is_telegram=is_telegram)
    if user is not None:
        customer_operator = ''
        warehouse = ''
        if hasattr(user, 'operator'):
            customer_operator = 'OPERATOR'
            warehouse = user.operator.warehouse
        elif hasattr(user, 'customer'):
            customer_operator = 'CUSTOMER'

        refresh = RefreshToken.for_user(user)
        response = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'data': {
                'full_name': user.full_name,
                # 'company_type': user.company_type,
                'warehouse': warehouse,
                'customer_operator': customer_operator
            }
        }
        if customer_operator == 'CUSTOMER':
            response['data']['language'] = user.customer.language
        return response
    else:
        raise APIValidation('invalid username or password', status_code=403)


def authenticate_telegram_user(request, is_telegram: bool = False):
    user = authenticate(request,
                        username=request.data['tg_id'],
                        is_telegram=is_telegram)
    if user is not None:
        customer_operator = ''
        warehouse = ''
        if hasattr(user, 'operator'):
            customer_operator = 'OPERATOR'
            warehouse = user.operator.warehouse
        elif hasattr(user, 'customer'):
            customer_operator = 'CUSTOMER'

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'data': {
                'full_name': user.full_name,
                'company_type': user.company_type,
                'warehouse': warehouse,
                'customer_operator': customer_operator
            }
        }
    else:
        raise APIValidation('invalid username or password', status_code=403)
