from cryptography import fernet
from django.contrib.auth.models import User
from django.db import models

from WebRAT.settings import WEBRAT_SECRET_KEY


class Credential(models.Model):
    """

    """

    def set_password(self, value: str):
        # TODO: If SECRET_KEY is moved to environment variable, change here, too
        f = fernet.Fernet(WEBRAT_SECRET_KEY)
        self._password = f.encrypt(value.encode())

    def get_password(self):
        # TODO: If SECRET_KEY is moved to environment variable, change here, too
        f = fernet.Fernet(WEBRAT_SECRET_KEY)
        return f.decrypt(self._password)

    def set_passphrase(self, value: str):
        # TODO: If SECRET_KEY is moved to environment variable, change here, too
        f = fernet.Fernet(WEBRAT_SECRET_KEY)
        self._passphrase = f.encrypt(value.encode())

    def get_passphrase(self):
        # TODO: If SECRET_KEY is moved to environment variable, change here, too
        f = fernet.Fernet(WEBRAT_SECRET_KEY)
        return f.decrypt(self._passphrase)

    def set_key(self, value: str):
        # TODO: If SECRET_KEY is moved to environment variable, change here, too
        f = fernet.Fernet(WEBRAT_SECRET_KEY)
        self._key = f.encrypt(value.encode())

    def get_key(self):
        # TODO: If SECRET_KEY is moved to environment variable, change here, too
        f = fernet.Fernet(WEBRAT_SECRET_KEY)
        return f.decrypt(self._key)

    name = models.TextField()
    notes = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField('nodes.Tag')  # name used as string to avoid circular imports
    username = models.TextField(default='root')
    _password = models.BinaryField(null=True, blank=True)
    password = property(get_password, set_password)
    _passphrase = models.BinaryField(null=True, blank=True)
    passphrase = property(get_passphrase, set_passphrase)
    _key = models.BinaryField(null=True, blank=True)
    key = property(get_key, set_key)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # TODO: Add keytype as a field (choice field)
    # keytype = models.   RSS, DSS/DSA, ECDSA, Ed25519
