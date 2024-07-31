from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet
from decouple import config

ENCRYPTION_KEY = config('ENCRYPTION_KEY')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    encrypted_api_key = models.BinaryField()
    encrypted_api_secret = models.BinaryField()

    def set_api_key(self, api_key):
        fernet = Fernet(ENCRYPTION_KEY)
        self.encrypted_api_key = fernet.encrypt(api_key.encode())

    def get_api_key(self):
        fernet = Fernet(ENCRYPTION_KEY)
        return fernet.decrypt(self.encrypted_api_key).decode()

    def set_api_secret(self, api_secret):
        fernet = Fernet(ENCRYPTION_KEY)
        self.encrypted_api_secret = fernet.encrypt(api_secret.encode())

    def get_api_secret(self):
        fernet = Fernet(ENCRYPTION_KEY)
        return fernet.decrypt(self.encrypted_api_secret).decode()
