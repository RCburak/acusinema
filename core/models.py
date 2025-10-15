from django.db import models
from django.utils.text import slugify

class Acusinema(models.Model):
    title = models.CharField("Film Başlığı", max_length=200)
    genre = models.CharField("Tür", max_length=100)
    duration = models.PositiveIntegerField("Süre (dakika)", help_text="Filmin süresini dakika cinsinden girin.")
    rating = models.DecimalField("Puan", max_digits=3, decimal_places=1, help_text="Filmin puanını girin (Örn: 8.5).")
    poster = models.ImageField("Afiş", upload_to='posters/', help_text="Filmin afişini yükleyin.")
    created_at = models.DateTimeField("Eklenme Tarihi", auto_now_add=True)

    class Meta:
        verbose_name = "Acusinema Filmi"
        verbose_name_plural = "Acusinema Filmleri"
        ordering = ['-created_at']

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

class SiteSettings(models.Model):
    address = models.CharField("Adres", max_length=300, blank=True, null=True)
    email1 = models.EmailField("E-posta Adresi 1", blank=True, null=True)
    email2 = models.EmailField("E-posta Adresi 2", blank=True, null=True)
    instagram_url = models.URLField("Instagram URL", blank=True, null=True)
    map_iframe_src = models.URLField("Google Harita Gömme (iframe src) Linki", blank=True, null=True)
    class Meta:
        verbose_name = "Site Ayarı"
        verbose_name_plural = "Site Ayarları"
    def __str__(self):
        return "Genel Site Ayarları"

class ContactMessage(models.Model):
    name = models.CharField("Ad Soyad", max_length=100)
    email = models.EmailField("E-posta Adresi")
    subject = models.CharField("Konu", max_length=200)
    message = models.TextField("Mesaj")
    created_at = models.DateTimeField("Gönderilme Tarihi", auto_now_add=True)
    class Meta:
        verbose_name = "İletişim Mesajı"
        verbose_name_plural = "İletişim Mesajları"
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
class SliderImage(models.Model):
    image = models.ImageField("Slider Resmi", upload_to='slider_images/', help_text="Slider'da gösterilecek resim (Önerilen boyut: 1200x600 piksel).")
    title = models.CharField("Başlık", max_length=200, help_text="Resmin alt etiketi (SEO için önemli).")
    order = models.PositiveIntegerField("Sıralama", default=0, help_text="Resimlerin gösterilme sırası (küçükten büyüğe).")
    is_active = models.BooleanField("Aktif mi?", default=True, help_text="Bu resim slider'da gösterilsin mi?")

    class Meta:
        verbose_name = "Slider Resmi"
        verbose_name_plural = "Slider Resimleri"
        ordering = ['order'] # Resimleri sıralama numarasına göre sırala

    def __str__(self):
        return self.title
