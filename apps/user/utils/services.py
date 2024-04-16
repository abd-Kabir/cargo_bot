from rest_framework import status

from apps.user.models import Customer
from config.core.api_exceptions import APIValidation


def generate_exp_code(customers) -> str:
    """
    return code for EXP company
    Code will go on like E0001-E3000 then goes X0001 till infinity
    """
    e_customers_count = Customer.objects.only('user__company_type').filter(user__company_type__startswith='E').count()
    x_customers_count = Customer.objects.only('user__company_type').filter(user__company_type__startswith='X').count()
    if e_customers_count >= 3000:
        code = "X" + str(x_customers_count + 1).zfill(4)  # +1 customers count for increment of customer_code
    else:
        code = "E" + str(e_customers_count + 1).zfill(4)  # +1 customers count for increment of customer_code
    return code


def generate_gg_code(customers) -> str:
    """
    return code for GG company
    Code starts with GGA or GG end goes like 0001 till infinity
    """
    avia_customers_count = (Customer.objects.only('user__company_type', 'code')
                            .filter(user__company_type='GG', code__startswith='GGA')).latest('code')
    auto_customers_count = (Customer.objects.only('user__company_type', 'code')
                            .filter(user__company_type='GG', code__startswith='GG')
                            .exclude(code__startswith='GGA')).latest('code')
    if customers.get('user_type') == 'AVIA':
        code = "GGA" + str(avia_customers_count + 1).zfill(4)  # +1 customers count for increment of customer_code
    else:
        code = "GG" + str(auto_customers_count + 1).zfill(4)  # +1 customers count for increment of customer_code
    return code


def generate_customer_code(user, customers: dict) -> str:
    # TODO: wait some time if not needed for this func delete it
    company_type = user.company_type
    if company_type == 'GG':
        code = generate_gg_code(customers)
    else:
        code = generate_exp_code(customers)
    return code


def prefix_check(prefix, user_type, request):
    company_type = request.user.company_type

    if company_type == 'GG':
        if prefix == 'GG' and user_type == 'AUTO':
            return True
        elif prefix == 'GAGA' and user_type == 'AVIA':
            return True
        else:
            raise APIValidation("Wrong combination of prefix and user_type",
                                status_code=status.HTTP_400_BAD_REQUEST)
    elif company_type == 'EXP':
        if prefix in ['E', 'X'] and user_type == 'AUTO':
            return True
        elif prefix == 'M' and user_type == 'AVIA':
            return True
        else:
            raise APIValidation("Wrong combination of prefix and user_type",
                                status_code=status.HTTP_400_BAD_REQUEST)
    else:
        raise APIValidation("Permission not allowed", status_code=status.HTTP_403_FORBIDDEN)