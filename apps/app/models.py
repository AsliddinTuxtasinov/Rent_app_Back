from django.db import models

# from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Sum


# Product class
class Product(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.name}"
    

# Product Type class
class ProductType(models.Model):
    FORMAT = [
        ('metr', 'metr'),
        ('sm', 'sm'),
        ('komplekt', 'komplekt'),
        ('dona', 'dona'),
    ]
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    format = models.CharField(max_length=100, choices=FORMAT)
    # diametr = models.CharField(max_length=200,null=True,blank=True)
    price = models.FloatField()
    def __str__(self):
        return f"{self.product}"
    
    
# Client class

class Client(models.Model):
    name = models.CharField(max_length=200)
    passport = models.CharField(max_length=9, null=True, blank=True)
    phone = models.CharField(max_length=9)
    desc = models.TextField(null=True, blank=True)
    @property
    def transactions(self):
        outcomes = Outcome.objects.filter(client=self)
        incomes = Income.objects.filter(client=self)
        
        outcome_data = [
            {
                'id': outcome.id,
                'product_name': outcome.product_name,
                'count': outcome.count,
                'date': outcome.date,
                'total': outcome.total
            }
            for outcome in outcomes
        ]
        
        income_data = [
            {
                'id': income.id,
                'product_name': income.product_name,
                'count': income.count,
                'date': income.date,
                'total': income.total
            }
            for income in incomes
        ]

        return {
            'outcomes': outcome_data,
            'incomes': income_data
        }
    



        
    def delete_completed(self):
        if self.status == "Shartnoma yakunlangan" and self.debt_product == 0:
            three_days_ago = timezone.now() - timezone.timedelta(minutes=3)
            if self.income.filter(date__lte=three_days_ago).exists():
                return
            self.delete()
    
    
    def __str__(self):
        return f"{self.name}"
    
# Rent class

class Rent(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True, blank=True)
    @property
    def client_name(self):
        return self.client.name
    @property
    def debt_product(self):
        count_out = sum(outcome.count for outcome in self.outcome.all())
        count_in = sum(income.count for income in self.income.all())
        return count_in - count_out
    
    def __str__(self):
        return f"{self.client.name}"

    
# Outcome class

class Outcome(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    count = models.FloatField()
    price = models.PositiveBigIntegerField(null=True, blank=True)
    date = models.DateTimeField()
    
    
        
    @property
    def total(self):
        if self.price is not None and self.price > 0:
            return self.price * self.count
        elif self.product.price is not None:
            return self.product.price * self.count
        else:
            return 0
    @property
    def client_name(self):
        return self.client.name
    
    @property
    def rent_name(self):
        return self.rent.client_name
    
    @property
    def product_name(self):
        return self.product.name
    
    
    
    def __str__(self):
        return f"{self.client.name}, {self.product.name} - {self.count}"


    
class Income(models.Model):
    class PayType(models.TextChoices):
        MAXSUS = "Maxsus to'lov", "Maxsus to'lov"
        TOLIQ = "To'liq yopish", "To'liq yopish"
    pay_type = models.CharField(max_length=30, choices=PayType.choices, null=True, blank=True)
    rent = models.ForeignKey(Rent, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    count = models.PositiveBigIntegerField()
    pay = models.PositiveBigIntegerField(null=True, blank=True)
    day = models.IntegerField()
    date = models.DateTimeField()

    @property
    def client_name(self):
        return self.client.name
    
    @property
    def rent_name(self):
        return self.rent.client_name
    
    @property
    def product_name(self):
        return self.product.name
    
    
    @property
    def total(self):
        if self.pay is not None and self.pay > 0:
            return self.pay * self.count
        elif self.product.price is not None:
            return self.product.price * self.count
        else:
            return 0
        
    
    # @property
    # def debt_days(self):
    #     today = timezone.localdate()
    #     days_overdue = (today - ).days
    #     return today
    
    def __str__(self):
        return f"{self.client.name}, {self.product.name} - {self.count}"
