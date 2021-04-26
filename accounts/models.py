import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image


class User(AbstractUser):
    def image_path_and_rename(self, filename):
        upload_to = 'profile_images'
        name = str(self.first_name) + " " + self.username
        new_name = name.replace(" ", "-") + "." + filename.split(".")[-1]
        return os.path.join(upload_to, new_name)

    USER_TYPE_CHOICES = (
        (1, 'Patient'),
        (2, 'External_Doctor'),
        (3, 'Nurse'),
        (4, 'Internal_Doctor'),
        (5, 'Lab_Officer'),
        (6, 'Small-Admin'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=1)
    image = models.ImageField(default='default.png', upload_to=image_path_and_rename)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)




class Patient(models.Model):
    BLOOD_GROUPS = (
        ('0 Rh-', '0 Rh-'),
        ('0 Rh+', '0 Rh+'),
        ('A Rh-', 'A Rh-'),
        ('A Rh+', 'A Rh+'),
        ('B Rh-', 'B Rh-'),
        ('B Rh+', 'B Rh+'),
        ('AB Rh-', 'AB Rh-'),
        ('AB Rh+', 'AB Rh+'),
    )
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    blood_group = models.CharField(
        max_length=7,
        choices=BLOOD_GROUPS,
        blank=True,
        null=True
    )
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}-Profile'

department = (
    ('Dentistry', "Dentistry"),
    ('Cardiology', "Cardiology"),
    ('ENT Specialists', "ENT Specialists"),
    ('Astrology', 'Astrology'),
    ('Neuroanatomy', 'Neuroanatomy'),
    ('Blood Screening', 'Blood Screening'),
    ('Eye Care', 'Eye Care'),
    ('Physical Therapy', 'Physical Therapy'),
)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    phone_number = models.CharField(max_length=20, unique=True, null=True, error_messages={
                                        'unique': "A user with that phone number already exists."
                                    })
    identification_number = models.CharField(
        max_length=11,
        unique=True,
    )
    department = models.CharField(choices=department, null=True, max_length=100)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username}- Dr'


