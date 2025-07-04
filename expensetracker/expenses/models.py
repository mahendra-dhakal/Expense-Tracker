from django.db import models
from django.contrib.auth.models import User 
# Create your models here.


class TransactionTypeChoices(models.TextChoices):
    CREDIT= 'credit', 'Credit'
    DEBIT= 'debit', 'Debit'

class TaxTypeChoices(models.TextChoices):
    FLAT= 'flat', 'Flat'
    PERCENTAGE= 'percentage', 'Percentage'

class TimestampedModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract= True

class ExpenseIncome(TimestampedModel):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description=models.TextField()
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type=models.CharField(max_length=20, choices=TransactionTypeChoices.choices, default=TransactionTypeChoices.CREDIT)
    tax=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_type=models.CharField(max_length=20, choices=TaxTypeChoices.choices, default=TaxTypeChoices.FLAT)

    @property
    def total(self):
        if self.tax_type == 'flat':
            return self.amount + self.tax
        else:
            return self.amount + (self.amount * self.tax / 100)
    
    def __str__(self):
        return f"{self.title} - {self.amount}"
