from django.db import models

class Parent(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    number = models.CharField(max_length=15)
    email = models.EmailField()
    class Meta:
        db_table = 'students_guardians'

# Create your models here.
