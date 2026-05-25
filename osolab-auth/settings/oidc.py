# -*- coding: utf-8 -*-
import base64
import json
import time

import requests
from django.core.exceptions import SuspiciousOperation
from requests.auth import HTTPBasicAuth

from taiga_contrib_oidc_auth.oidc import TaigaOIDCAuthenticationBackend


class OsolabTaigaOIDCAuthenticationBackend(TaigaOIDCAuthenticationBackend):
    def verify_token(self, token, **kwargs):
        if not self.get_settings("OIDC_OSOLAB_SKIP_ID_TOKEN_SIGNATURE", False):
            return super().verify_token(token, **kwargs)

        parts = token.split(".")
        if len(parts) != 3:
            raise SuspiciousOperation("Invalid ID token format.")

        payload_segment = parts[1]
        padding = "=" * (-len(payload_segment) % 4)
        payload_data = base64.urlsafe_b64decode(payload_segment + padding)
        payload = json.loads(payload_data.decode("utf-8"))

        nonce = kwargs.get("nonce")
        if self.get_settings("OIDC_USE_NONCE", True) and nonce != payload.get("nonce"):
            raise SuspiciousOperation("JWT Nonce verification failed.")

        audience = payload.get("aud")
        if audience != self.OIDC_RP_CLIENT_ID:
            raise SuspiciousOperation("JWT audience verification failed.")

        expires_at = payload.get("exp")
        if not isinstance(expires_at, int) or expires_at <= int(time.time()):
            raise SuspiciousOperation("JWT expiration verification failed.")

        return payload

    def get_token(self, payload):
        auth = None
        if self.get_settings("OIDC_TOKEN_USE_BASIC_AUTH", False):
            user = payload.get("client_id")
            password = payload.get("client_secret")

            auth = HTTPBasicAuth(user, password)
            del payload["client_secret"]

        response = requests.post(
            self.OIDC_OP_TOKEN_ENDPOINT,
            data=payload,
            auth=auth,
            headers={"x-flow-type": "AuthorizationCode"},
            verify=self.get_settings("OIDC_VERIFY_SSL", True),
            timeout=self.get_settings("OIDC_TIMEOUT", None),
            proxies=self.get_settings("OIDC_PROXY", None),
        )
        self.raise_token_response_error(response)
        return response.json()
