from django.db import models
from .constants import TRANSACTION_TYPE

class Transaction(models.Model):
    account = models.ForeignKey('customers.UserBankAccount', related_name='transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

class Adopt(models.Model):
    user_account = models.ForeignKey('customers.UserBankAccount', on_delete=models.CASCADE)
    pet = models.ForeignKey('pets.Pet', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    adopt_date = models.DateTimeField(auto_now_add=True)
    adopt_price = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_adopting_book = models.DecimalField(decimal_places=2, max_digits=12, null=True, blank=True)

    def is_returned(self):
        return self.return_date is not None

    def __str__(self):
        return f'{self.user_account.user.username} - {self.pet.pet_title}'

