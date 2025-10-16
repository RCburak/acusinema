# users/models.py

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import uuid # Benzersiz kod için eklendi

class CustomUserManager(BaseUserManager):
    # Bu kısım aynı kalabilir...
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
        # Süper kullanıcıların e-postası doğrulanmış ve aktif başlasın
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_email_verified', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Süper kullanıcının is_staff=True olması gerekir.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Süper kullanıcının is_superuser=True olması gerekir.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('e-posta adresi', unique=True)
    first_name = models.CharField('ad', max_length=150, blank=True)
    last_name = models.CharField('soyad', max_length=150, blank=True)
    is_staff = models.BooleanField(
        'personel durumu',
        default=False,
        help_text='Kullanıcının admin sitesine giriş yapıp yapamayacağını belirtir.',
    )
    # Yeni kullanıcılar doğrulanana kadar aktif olmayacak
    is_active = models.BooleanField(
        'aktif',
        default=False,
        help_text='Hesap doğrulanana kadar bu alan false kalır.',
    )
    date_joined = models.DateTimeField('katılım tarihi', default=timezone.now)

    # === YENİ EKLENEN ALANLAR ===
    is_email_verified = models.BooleanField('e-posta doğrulandı', default=False)
    verification_code = models.CharField('doğrulama kodu', max_length=100, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def save(self, *args, **kwargs):
        # Yeni kullanıcı oluşturulurken benzersiz bir kod ata
        if not self.pk and not self.verification_code:
            self.verification_code = str(uuid.uuid4())
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email