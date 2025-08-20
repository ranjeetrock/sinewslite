from django.db import models
from cloudinary_storage.storage import RawMediaCloudinaryStorage


class PatrakaarMitra(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    CATEGORY_CHOICES = [
        ('Patrakaar', 'Patrakaar Mitra'),
        ('Reporter', 'Reporter'),
        ('Cameraman', 'Cameraman'),
        ('Member', 'Member'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    activity = models.TextField(blank=True, null=True)
    address = models.TextField()

    def __str__(self):
        return self.name


class ENewsPaper(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(
        storage=RawMediaCloudinaryStorage(),  # uses Cloudinary Raw storage
        blank=True,
        null=True
    )
    published_on = models.DateField(blank=True, null=True)
    uploaded_by = models.CharField(max_length=100, default="Administration")

    class Meta:
        ordering = ['-published_on']  # show latest first

    def __str__(self):
        return self.title or f"ENewsPaper #{self.pk or 'new'}"
