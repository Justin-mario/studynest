"""Smoke tests — confirms the app boots and the public landing page renders."""
from __future__ import annotations

from flask.testing import FlaskClient


def test_landing_page_renders(client: FlaskClient) -> None:
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"StudyNest" in resp.data


def test_sign_in_page_renders(client: FlaskClient) -> None:
    resp = client.get("/auth/sign-in")
    assert resp.status_code == 200


def test_protected_route_redirects_to_sign_in(client: FlaskClient) -> None:
    resp = client.get("/dashboard/", follow_redirects=False)
    assert resp.status_code in (301, 302)
