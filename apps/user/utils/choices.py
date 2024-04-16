from django.utils.translation import gettext_lazy as _

# CUSTOMERS
AUTO = 'AUTO'
AVIA = 'AVIA'
CAR_OR_AIR_CHOICE = [
    (AUTO, _('Auto')),
    (AVIA, _('Avia'))
]
GG = 'GG'
EXP = 'EXP'
COMPANY_TYPE_CHOICES = [
    (GG, GG),
    (EXP, EXP),
]
E = 'E'
M = 'M'
X = 'X'
GG = 'GG'
GAGA = 'GAGA'
PREFIX_CHOICES = [
    (E, E),
    (M, M),
    (X, X),
    (GG, GG),
    (GAGA, GAGA),
]
# OPERATORS
WEB = 'WEB'
TELEGRAM = 'TELEGRAM'
WEB_OR_TELEGRAM_CHOICE = [
    (WEB, _('Web')),
    (TELEGRAM, _('Telegram'))
]
TASHKENT = 'TASHKENT'
CHINA = 'CHINA'
WAREHOUSE_CHOICE = [
    (TASHKENT, _('Tashkent')),
    (CHINA, _('China'))
]