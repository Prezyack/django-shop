# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from shop import app_settings

if app_settings.GOOGLE_RECAPTCHA:

    import requests
    from django.utils.translation import ugettext_lazy as _
    from rest_framework import serializers, exceptions
    from rest_auth.serializers import LoginSerializer as BaseLoginSerializer

    class LoginSerializer(BaseLoginSerializer):
        SITE_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'

        recaptcha_response = serializers.CharField(required=False, allow_blank=True)

        def validate(self, attrs):
            post_data = {
                'secret': app_settings.GOOGLE_RECAPTCHA['SECRET'],
                'response': attrs.get('recaptcha_response'),
                'remoteip': self.context['request'].META['REMOTE_ADDR']
            }
            response = requests.post(self.SITE_VERIFY_URL, data=post_data).json()
            if not response.get('success'):
                msg = _("reCaptcha did not validate. Reason: {}.")
                raise exceptions.ValidationError(msg.format(response.get('error-codes')))

            return super(LoginSerializer, self).validate(attrs)

else:
    # if reCaptcha is deactivated, fall back to the default LoginSerializer
    from rest_auth.serializers import LoginSerializer
