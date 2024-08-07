from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

from config.core.choices import COMPANY_TYPE_CHOICES, GG, CAR_OR_AIR_CHOICE, WEB_OR_TELEGRAM_CHOICE, \
    WAREHOUSE_CHOICE, PREFIX_CHOICES, CUSTOMER_REGISTRATION_STATUS, WAITING
from config.models import BaseModel

username_validator = UnicodeUsernameValidator()


class User(AbstractUser):
    first_name = None
    last_name = None
    password = models.CharField(_("password"), max_length=128, null=True, blank=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Обязательно. Не более 150 символов. Только буквы, цифры и @/./+/-/_."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("Пользователь с таким именем уже существует."),
        },
        null=True, blank=True
    )
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    full_name = models.CharField(_("full name"), max_length=255, null=True, blank=True)
    company_type = models.CharField(_("company type"), max_length=5, choices=COMPANY_TYPE_CHOICES, default=GG)

    class Meta:
        db_table = 'User'


class Customer(BaseModel):
    prefix = models.CharField("prefix", max_length=6, choices=PREFIX_CHOICES, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True)
    debt = models.FloatField(default=0)
    phone_number = models.CharField(_("phone number"), max_length=35, null=True, blank=True)
    tg_id = models.CharField(max_length=155, null=True, blank=True)
    language = models.CharField(max_length=2, choices=settings.LANGUAGES, default='uz')
    location = models.JSONField(null=True, blank=True)

    user_type = models.CharField(_("user type"), max_length=4, choices=CAR_OR_AIR_CHOICE)
    passport_photo = models.ForeignKey("files.File", on_delete=models.SET_NULL,
                                       null=True, blank=True)  # if user_type==AVIA
    birth_date = models.DateField(null=True, blank=True)  # if user_type==AVIA
    passport_serial_number = models.CharField(max_length=100, null=True, blank=True)  # if user_type==AVIA
    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='customers_accepted_by',
                                    null=True, blank=True)
    accepted_time = models.DateTimeField(null=True, blank=True)
    about_customer = models.TextField(null=True, blank=True)

    is_data_transferred = models.BooleanField(default=False)
    ex_prefix = models.CharField("prefix", max_length=6, choices=PREFIX_CHOICES, null=True, blank=True)
    ex_code = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')

    class Meta:
        # unique_together = ['prefix', 'code']
        db_table = 'Customer'
        constraints = [
            models.UniqueConstraint(fields=['prefix', 'code'], name='unique_prefix_code'),
            models.UniqueConstraint(
                fields=['user_type', 'phone_number'], name='unique_user_type_phone_number'
            ),
        ]


class Operator(BaseModel):
    # Type(Telegram / Web)

    tg_id = models.CharField(max_length=155, unique=True, null=True, blank=True)
    operator_type = models.CharField(_("operator type"), max_length=8, choices=WEB_OR_TELEGRAM_CHOICE)
    warehouse = models.CharField(_("warehouse"), max_length=8, choices=WAREHOUSE_CHOICE, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='operator')

    class Meta:
        db_table = 'Operator'


class CustomerRegistration(BaseModel):
    reject_message = models.TextField(null=True, blank=True)
    step = models.SmallIntegerField(default=1)
    done = models.BooleanField(default=False)
    status = models.CharField(choices=CUSTOMER_REGISTRATION_STATUS, default=WAITING)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, related_name='customer_registrations',
                                 null=True, blank=True)

    # registration_screenshots on File model
    class Meta:
        db_table = 'CustomerRegistration'
