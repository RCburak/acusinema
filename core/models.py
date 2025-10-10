# core/models.py

from django.db import models
from django.utils.text import slugify

class Acusinema(models.Model):
    GENRE_CHOICES = [
        ('DRAM', 'Dram'),
        ('GERILIM', 'Gerilim'),
        ('BILIM_KURGU', 'Bilim Kurgu'),
        ('MACERA', 'Macera'),
        ('KOMEDI', 'Komedi'),
        ('AKSIYON', 'Aksiyon'),
        ('FANTASTIK', 'Fantastik'),
        ('KORKU', 'Korku'),
    ]

    title = models.CharField("Film Başlığı", max_length=200)
    genre = models.CharField("Tür", max_length=20, choices=GENRE_CHOICES, default='DRAM')
    duration = models.PositiveIntegerField("Süre (dakika)", help_text="Filmin süresini dakika cinsinden girin.")
    rating = models.DecimalField("Puan", max_digits=3, decimal_places=1, help_text="Filmin puanını girin (Örn: 8.5).")
    poster = models.ImageField("Afiş", upload_to='posters/', help_text="Filmin afişini yükleyin.")
    
    class Meta:
        verbose_name = "Acusinema Filmi"
        verbose_name_plural = "Acusinema Filmleri"
        ordering = ['-rating']

    def __str__(self):
        return self.title

class Event(models.Model):
    LOCATION_CHOICES = [
        ('K_SALONU', 'Konferans Salonu'),
        ('ACIK_HAVA', 'Açık Hava Sineması'),
    ]
    title = models.CharField("Etkinlik Başlığı", max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField("Açıklama")
    event_date = models.DateTimeField("Etkinlik Tarihi ve Saati")
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