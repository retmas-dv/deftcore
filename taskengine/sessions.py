__author__ = 'Dmitry Golubkov'

from django.contrib.sessions.base_session import AbstractBaseSession
from django.contrib.sessions.backends.db import SessionStore as DBStore


class CustomSession(AbstractBaseSession):
    @classmethod
    def get_session_store_class(cls):
        return SessionStore

    class Meta:
        db_name = 'deft_adcr'
        db_table = '"ATLAS_DEFT"."DJANGO_SESSION"'


class SessionStore(DBStore):
    @classmethod
    def get_model_class(cls):
        return CustomSession
