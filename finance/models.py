# Create a Settlement class
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Settlement(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)
    status = models.IntegerField()
    image = models.CharField(max_length=100)


class RecentTransaction(models.Model):
    name = models.CharField(max_length=100)
    status = models.IntegerField()
    price = models.CharField(max_length=100)
    flag = models.IntegerField(default=0)


class Comment(models.Model):
    settlement = models.ForeignKey(Settlement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Field to track the last updated time

    def __str__(self):
        return f"Comment by {self.user.username} on {self.created_at}"


class Category(models.Model):
    name = models.CharField(max_length=50)


class Transaction(models.Model):
    transaction_number = models.CharField(max_length=30, unique=True)
    purpose = models.CharField(max_length=50)
    categoryField = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    amount = models.FloatField()

    def __str__(self):
        return self.purpose

    def get_absolute_url(self):
        return reverse("finance:updateTransaction", args=[self.transaction_number])

    def save(self, *args, **kwargs):
        if not self.transaction_number:
            last_transaction = Transaction.objects.order_by('-id').first()

            if last_transaction and last_transaction.transaction_number:
                last_number = int(last_transaction.transaction_number)
                new_number = last_number + 1
                potential_transaction_number = f'{new_number:03d}'  # Generate the potential transaction number

                # Check if this potential number already exists in the database
                while Transaction.objects.filter(transaction_number=potential_transaction_number).exists():
                    new_number += 1
                    potential_transaction_number = f'{new_number:03d}'

                self.transaction_number = potential_transaction_number
            else:
                self.transaction_number = '001'  # Starting number if no transactions exist

        super(Transaction, self).save(*args, **kwargs)


class Budgets(models.Model):
    date = models.DateField(auto_now_add=True)
    amount = models.CharField(max_length=100)


regular_user = {"username": "ankit", "password": "regular"}
