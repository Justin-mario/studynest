"""WSGI entry point for production (alwaysdata.com).

alwaysdata's Python sites point to a WSGI callable named `application`.
"""
from app import create_app

application = create_app()
