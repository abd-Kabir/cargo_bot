import requests
import xml.etree.ElementTree as ET
from django.conf import settings

from apps.integrations.models import OrderEMU

emu_integration = settings.INTEGRATIONS['EMU']


def emu_auth():
    url = 'https://home.courierexe.ru/api/'
    emu_creds = emu_integration['credentials']
    emu_extra = emu_integration['extra']
    xml = f"""
    <auth extra="{emu_extra}" login="{emu_creds['username']}" pass="{emu_creds['password']}"></auth>
    """
    headers = {'Content-Type': 'application/xml'}
    response = requests.post(url, data=xml, headers=headers)
    return response


def emu_order(order_id, customer_full_name, order_instance: OrderEMU):
    load = order_instance.load
    url = 'https://home.courierexe.ru/api/'

    emu_creds = emu_integration['credentials']
    emu_extra = emu_integration['extra']

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<neworder>
    <auth extra="{emu_extra}" login="{emu_creds['username']}" pass="{emu_creds['password']}"></auth>
    <order orderno="{order_id}">
        <barcode>{order_id}</barcode>
        <sender>
            <company>Express Cargo</company>
            <phone>+998 98 363 37 67</phone>
            <town>814303</town>
            <address>Arnasay 7A</address>
        </sender>
        <receiver>
            <person>{customer_full_name}</person>
            <phone>{order_instance.phone_number}</phone>
            <town>{order_instance.town}</town>
            <address>{order_instance.address}</address>
        </receiver>
        <service>{order_instance.service}</service>
        <items>
            <item length="0" height="0" width="0" quantity="{load.products.count()}" mass="{load.weight}" retprice="0">Посылка Express cargo</item>
        </items>
    </order>
</neworder>"""

    headers = {'Content-Type': 'application/xml'}
    response = requests.post(url, data=xml.encode('utf-8'), headers=headers)
    return response


def emu_towns():
    url = 'https://home.courierexe.ru/api/'
    xml = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <townlist>
        <conditions>
            <country>1219</country>
        </conditions>
    </townlist>
    """

    headers = {'Content-Type': 'application/xml'}
    response = requests.post(url, data=xml, headers=headers)
    return response


def emu_streets(town):
    url = 'https://home.courierexe.ru/api/'
    xml = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <streetlist>
        <conditions>
            <town>{town}</town>
        </conditions>
    </streetlist>
    """

    headers = {'Content-Type': 'application/xml'}
    response = requests.post(url, data=xml, headers=headers)
    return response


def emu_tracking():
    xml = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <tracking>
        <extra>8</extra>
        <orderno>1234</orderno>
    </tracking>
    """
