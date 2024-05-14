from rest_framework import serializers

from config.core.api_exceptions import APIValidation


class SettingToolSerializer(serializers.Serializer):
    avia = serializers.CharField(allow_null=True, required=False)
    auto = serializers.CharField(allow_null=True, required=False)


class PaymentCardToolSerializer(serializers.Serializer):
    avia = serializers.CharField(allow_null=True, required=False)
    auto = serializers.CharField(allow_null=True, required=False)

    @staticmethod
    def get_avia(value):
        if value:
            if value.isdigit():
                p_card = value.replace(' ', '')
            else:
                raise APIValidation('Payment card includes only digits (payment-card 16 digits)')
            if len(p_card) != 16:
                raise APIValidation('Payment card should have 16 digits')
            return p_card
        return value

    @staticmethod
    def get_auto(value):
        if value:
            if value.isdigit():
                p_card = value.replace(' ', '')
            else:
                raise APIValidation('Payment card includes only digits (payment-card 16 digits)')
            if len(p_card) != 16:
                raise APIValidation('Payment card should have 16 digits')
            return p_card
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['avia'] = self.get_avia(representation['avia'])
        representation['auto'] = self.get_auto(representation['auto'])
        return representation


class SettingsSerializer(serializers.Serializer):
    payment_card = PaymentCardToolSerializer(required=False)
    price = SettingToolSerializer(required=False)
    address = SettingToolSerializer(required=False)
    link = SettingToolSerializer(required=False)
    support = SettingToolSerializer(required=False)
