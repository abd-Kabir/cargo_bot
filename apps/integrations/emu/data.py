import requests
from django.conf import settings

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


def emu_order(order_id, customer, data):
    url = 'https://home.courierexe.ru/api/'

    emu_creds = emu_integration['credentials']
    emu_extra = emu_integration['extra']

    xml = f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <neworder newfolder="NO">
        <auth extra="{emu_extra}" login="{emu_creds['username']}" pass="{emu_creds['password']}"></auth>
        <order orderno="{order_id}">
            <barcode>{order_id}</barcode>
        </order>
        <receiver>
            <person>{customer['full_name']}</person>
            <phone>{customer['phone_number']}</phone>
            <town>{data['town']}</town>
            <address>Адрес получателя</address>
        </receiver>
    </neworder>
    """

    headers = {'Content-Type': 'application/xml'}
    response = requests.post(url, data=xml, headers=headers)
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
