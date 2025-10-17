# users/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import random
import string

class CustomUserManager(BaseUserManager):
    """
    E-posta adresi ile kullanıcı oluşturan özel kullanıcı yöneticisi.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Kullanıcıların bir e-posta adresi olmalıdır')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_email_verified', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Süper kullanıcının is_staff=True olması gerekir.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Süper kullanıcının is_superuser=True olması gerekir.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    E-postayı kullanıcı adı olarak kullanan özel kullanıcı modeli.
    """
    email = models.EmailField('e-posta adresi', unique=True)
    first_name = models.CharField('ad', max_length=150, blank=True)
    last_name = models.CharField('soyad', max_length=150, blank=True)
    is_staff = models.BooleanField(
        'personel durumu',
        default=False,
        help_text='Kullanıcının admin sitesine giriş yapıp yapamayacağını belirtir.',
    )
    is_active = models.BooleanField(
        'aktif',
        default=False, # Yeni kullanıcılar doğrulanana kadar aktif olmasın
        help_text='Bu kullanıcının aktif olarak kabul edilip edilmeyeceğini belirtir.',
    )
    date_joined = models.DateTimeField('katılım tarihi', default=timezone.now)

    # Yeni eklenen alanlar
    is_email_verified = models.BooleanField('e-posta doğrulandı', default=False)
    verification_code = models.CharField('doğrulama kodu', max_length=6, blank=True, null=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def generate_verification_code(self):
        self.verification_code = ''.join(random.choices(string.digits, k=6))
        self.save()