from typing import Literal

import requests

from simple_openid.client_authentication import AccessTokenBearerAuth
from simple_openid.data import (
    UserinfoErrorResponse,
    UserinfoRequest,
    UserinfoSuccessResponse,
)
from simple_openid.exceptions import OpenidProtocolError


def fetch_userinfo(
    userinfo_endpoint: str,
    access_token: str,
    http_method: Literal["GET", "POST"] = "GET",
) -> UserinfoSuccessResponse | UserinfoErrorResponse:
    request = UserinfoRequest()
    auth = AccessTokenBearerAuth(access_token)

    if http_method == "GET":
        response = requests.get(request.encode_url(userinfo_endpoint), auth=auth)
    elif http_method == "POST":
        response = requests.post(
            userinfo_endpoint, request.encode_x_www_form_urlencoded(), auth=auth
        )
    else:
        raise ValueError(f"argument http_method has unsupported value {http_method}")

    if response.headers["Content-Type"] != "application/json":
        raise OpenidProtocolError(
            f"userinfo request was responded with invalid Content-Type", response
        )

    if response.status_code == 200:
        return UserinfoSuccessResponse.parse_raw(response.content)
    else:
        return UserinfoErrorResponse.parse_raw(response.content)