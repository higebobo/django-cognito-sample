# -*- mode: python -*- -*- coding: utf-8 -*-
import secrets
import string

from jose import jwt
from django.conf import settings
from django.contrib.auth.models import (User, AnonymousUser)
from django_cognito.authentication.middleware import helpers as m_helpers

if getattr(settings, 'APP_SECRET_KEY'):
    from django_cognito.authentication.cognito.helpers import initiate_auth
else:
    from .helpers import initiate_auth


class AwsCognitoAuthentication:

    def authenticate(self, request, username=None, password=None):
        if username is None:
            user, _, _ = m_helpers.process_request(request)
            return user
        else:
            try:
                result = initiate_auth(
                    {
                        'username': username,
                        'password': password,
                        'auth_flow': 'USER_PASSWORD_AUTH'
                    }
                )
                try:
                    return User.objects.get(username=username)
                except User.DoesNotExist:
                    if settings.AUTO_CREATE_USER:
                        try:
                            is_staff = bool(settings.ADD_STAFF_ROLE)
                        except:
                            is_staff = False
                        params = {
                            'username': username,
                            'password': self.gen_password(),
                            'is_staff': is_staff
                        }
                        try:
                            token = result['AuthenticationResult']['IdToken']
                            _, user_info = self.parse_token_jwt(token)
                            email = user_info.get('email')
                            if email:
                                params.update({'email': email})
                            name = user_info.get('name')
                            if name:
                                name_list = name.split(' ')
                                if len(name_list) == 2:
                                    params.update(
                                        {
                                            'first_name': name_list[0],
                                            'last_name': name_list[1]
                                        }
                                    )
                        except Exception as e:
                            print(e)
                            pass
                        user = User.objects.create_user(**params)

                        return user

                    return AnonymousUser()
            except Exception as e:
                # print(e)
                return AnonymousUser()
        return AnonymousUser()

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def gen_password(self, with_symbol=True, length=12):
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
        if with_symbol:
            chars += '%&$#()'
        return ''.join(secrets.choice(chars) for x in range(length))

    def parse_token_jwt(self, token):
        header = jwt.get_unverified_header(token)
        claims = jwt.get_unverified_claims(token)
        return (header, claims)
