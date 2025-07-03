from django.db import models
import random
import string

# Create your models here.


class InquiryForm(models.Model):
    # Gender choices
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    # Marital status choices
    MARITAL_CHOICES = [
        ("single", "Single"),
        ("married", "Married"),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_CHOICES)
    unique_number = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Generate unique number if not provided
        if not self.unique_number:
            # First two letters of first name + first letter of last name + random number
            prefix = self.first_name[:2].upper() + self.last_name[:1].upper()
            random_num = random.randint(1000, 9999)
            self.unique_number = f"{prefix}{random_num}"
        super().save(*args, **kwargs)

    def get_salutation(self):
        # Logic for salutation based on gender and marital status
        if self.gender == "female" and self.marital_status == "married":
            return "Mrs"
        elif self.gender == "male" and self.marital_status == "married":
            return "Mr"
        elif self.gender == "female" and self.marital_status == "single":
            return "Miss"
        else:
            return "Mr"  # Default for single male

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.unique_number}"
