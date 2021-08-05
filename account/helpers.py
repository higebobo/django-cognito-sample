# -*- mode: python -*- -*- coding: utf-8 -*-
from django_cognito.authentication.cognito import constants
from django_cognito.authentication.cognito.base import (
    CognitoClient, CognitoException)


def initiate_auth(data, param_mapping=None):
    if ('username' in data and 'password' in data) \
            or ('username' in param_mapping and 'password' in param_mapping):
        auth_flow = constants.USER_PASSWORD_FLOW
        username = parse_parameter(data, param_mapping, 'username')
        password = parse_parameter(data, param_mapping, 'password')

        return initiate_auth_without_secret(username, auth_flow, password)

    else:
        raise ValueError('Unsupported auth flow')


def initiate_auth_without_secret(username, auth_flow, password=None,
                                 refresh_token=None, srp_a=None):
    auth_parameters = {}
    if auth_flow == constants.USER_PASSWORD_FLOW:
        auth_parameters['USERNAME'] = username
        auth_parameters['PASSWORD'] = password
    elif auth_flow == constants.REFRESH_TOKEN_AUTH_FLOW \
            or auth_flow == constants.REFRESH_TOKEN_FLOW:
        if refresh_token is None:
            raise Exception(
                'To use the refresh token flow you must provide a refresh token')
        else:
            auth_parameters['REFRESH_TOKEN'] = refresh_token
    else:
        raise Exception('Provided auth flow is not supported')

    try:
        return CognitoClient.client.initiate_auth(
            AuthFlow=auth_flow,
            ClientId=constants.CLIENT_ID,
            AuthParameters=auth_parameters)

    except constants.AWS_EXCEPTIONS as ex:
        raise CognitoException.create_from_exception(ex)


def parse_parameter(data, param_mapping, param=None):
    if param_mapping is not None:
        if param in param_mapping:
            return data[param_mapping[param]]
    else:
        return data[param]
