# core/models.py

from django.db import models
from django.utils.text import slugify

class Acusinema(models.Model):
    title = models.CharField("Movie Title", max_length=200)
    genre = models.CharField("Genre", max_length=100)
    duration = models.PositiveIntegerField("Duration (minutes)", help_text="Enter the movie duration in minutes.")
    rating = models.DecimalField("Rating", max_digits=3, decimal_places=1, help_text="Enter the movie rating (e.g., 8.5).")
    poster = models.ImageField("Poster", upload_to='posters/', help_text="Upload the movie poster.")
    created_at = models.DateTimeField("Date Added", auto_now_add=True)
    
    class Meta:
        verbose_name = "Acusinema Movie"
        verbose_name_plural = "Acusinema Movies"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Event(models.Model):
    LOCATION_CHOICES = [
        ('CONFERENCE_HALL', 'Conference Hall'),
        ('OPEN_AIR_CINEMA', 'Open-Air Cinema'),
    ]
    title = models.CharField("Event Title", max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    description = models.TextField("Description")
    event_date = models.DateTimeField("Event Date and Time")
    location = models.CharField("Location", max_length=20, choices=LOCATION_CHOICES, default='CONFERENCE_HALL')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['event_date']
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class SiteSettings(models.Model):
    address = models.CharField("Address", max_length=300, blank=True, null=True)
    email1 = models.EmailField("Email Address 1", blank=True, null=True)
    email2 = models.EmailField("Email Address 2", blank=True, null=True)
    instagram_url = models.URLField("Instagram URL", blank=True, null=True)
    map_iframe_src = models.URLField("Google Maps Embed (iframe src) Link", blank=True, null=True)
    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"
    def __str__(self):
        return "General Site Settings"

class ContactMessage(models.Model):
    name = models.CharField("Full Name", max_length=100)
    email = models.EmailField("Email Address")
    subject = models.CharField("Subject", max_length=200)
    message = models.TextField("Message")
    created_at = models.DateTimeField("Date Sent", auto_now_add=True)
    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']
    def __str__(self):
        return f"{self.name} - {self.subject}"

class SliderImage(models.Model):
    image = models.ImageField("Slider Image", upload_to='slider_images/', help_text="Image to be displayed in the slider.")
    title = models.CharField("Title", max_length=200, help_text="Image alt text (important for SEO).")
    order = models.PositiveIntegerField("Order", default=0, help_text="Display order of images (from small to large).")
    is_active = models.BooleanField("Is Active?", default=True, help_text="Should this image be shown in the slider?")
    class Meta:
        verbose_name = "Slider Image"
        verbose_name_plural = "Slider Images"
        ordering = ['order']
    def __str__(self):
        return self.title