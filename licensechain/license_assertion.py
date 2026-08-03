"""Verify LicenseChain license_token (RS256) via JWKS."""

from __future__ import annotations

from typing import Any, Dict, Optional

LICENSE_TOKEN_USE_CLAIM = "licensechain_license_v1"


def verify_license_assertion_jwt(
    token: str,
    jwks_url: str,
    *,
    expected_app_id: Optional[str] = None,
    issuer: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Verify license_token from POST /v1/licenses/verify using license_jwks_uri or GET /v1/licenses/jwks.

    Requires: PyJWT and cryptography (see requirements.txt).
    """
    import jwt
    from jwt import PyJWKClient

    jwks_client = PyJWKClient(jwks_url)
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    decode_kw: Dict[str, Any] = {
        "algorithms": ["RS256"],
        "options": {"verify_aud": False},
    }
    if issuer:
        decode_kw["issuer"] = issuer
    payload = jwt.decode(token, signing_key.key, **decode_kw)
    if payload.get("token_use") != LICENSE_TOKEN_USE_CLAIM:
        raise ValueError(f'Invalid license token: expected token_use "{LICENSE_TOKEN_USE_CLAIM}"')
    if expected_app_id is not None and expected_app_id != "" and payload.get("aud") != expected_app_id:
        raise ValueError("Invalid license token: aud does not match expected app id")
    return payload
