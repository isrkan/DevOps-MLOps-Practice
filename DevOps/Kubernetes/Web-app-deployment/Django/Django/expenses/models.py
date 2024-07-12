from django.db import models

# Create your models here.
class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    approved = models.BooleanField(default=False)
    added_by = models.CharField(max_length=255)

    class Meta:
        db_table = 'expense'  # Name of the existing table in PostgreSQL