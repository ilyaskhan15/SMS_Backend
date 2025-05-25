from django.db import models

class Parent(models.Model):
    first_name = models.CharField(max_length=100, null=False, blank=False, db_index=True)
    last_name = models.CharField(max_length=100, null=False, blank=False, db_index=True)
    number = models.CharField(max_length=15)
    email = models.EmailField()
    class Meta:
        db_table = 'students_guardians'
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.number})"

# Create your models here.
