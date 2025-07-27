from django.db import models

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
