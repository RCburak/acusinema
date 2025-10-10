# core/models.py

from django.db import models
from django.utils.text import slugify

# ... (Acusinema modeliniz burada aynı kalıyor) ...
class Acusinema(models.Model):
    title = models.CharField("Film Başlığı", max_length=200)
    director = models.CharField("Yönetmen", max_length=100)
    release_date = models.DateField("Yayın Tarihi")
    
    class Meta:
        verbose_name = "Acusinema Filmi"
        verbose_name_plural = "Acusinema Filmleri"

    def __str__(self):
        return self.title


# --- İSTEDİĞİNİZ YENİ SEÇENEKLERLE GÜNCELLENMİŞ EVENT MODELİ ---
class Event(models.Model):
    
    # İstediğiniz yeni seçenekleri doğru formatta yazıyoruz
    LOCATION_CHOICES = [
        ('K_SALONU', 'Konferans Salonu'),
        ('ACIK_HAVA', 'Açık Hava Sineması'),
    ]

    title = models.CharField("Etkinlik Başlığı", max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True, help_text="Bu alan otomatik olarak doldurulacaktır.")
    description = models.TextField("Açıklama")
    event_date = models.DateTimeField("Etkinlik Tarihi ve Saati")
    # choices parametresi yeni listemizi kullanacak şekilde güncellendi
    location = models.CharField("Konum", max_length=10, choices=LOCATION_CHOICES, default='K_SALONU')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Etkinlik"
        verbose_name_plural = "Etkinlikler"
        ordering = ['event_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)