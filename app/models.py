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
    def get_all_transactions(self):
        income_records = Income.objects.filter(client=self)
        outcome_records = Outcome.objects.filter(client=self)
        transactions = {
            'outcome': {},
            'income': {},
            'debt_counts': {},
            'total_income': {'count': 0, 'total': 0},  # Add total income
            'total_outcome': {'count': 0, 'total': 0},  # Add total outcome
        }

        # Calculate total outcome counts and total amount for each product
        total_outcome_counts = {}
        total_outcome_amounts = {}
        for outcome in outcome_records:
            product_name = outcome.product.name
            count = outcome.count
            total_outcome_counts[product_name] = total_outcome_counts.get(product_name, 0) + count
            total_outcome_amounts[product_name] = total_outcome_amounts.get(product_name, 0) + outcome.total

        # Calculate total income counts and total amount for each product
        total_income_counts = {}
        total_income_amounts = {}
        for income in income_records:
            product_name = income.product.name
            count = income.count
            total_income_counts[product_name] = total_income_counts.get(product_name, 0) + count
            total_income_amounts[product_name] = total_income_amounts.get(product_name, 0) + income.total

        # Calculate total income count and amount
        transactions['total_income']['total'] = sum(total_income_amounts.values())
        transactions['total_income']['count'] = sum(total_income_counts.values())
        

        # Calculate total outcome count and amount
        transactions['total_outcome']['total'] = sum(total_outcome_amounts.values())
        transactions['total_outcome']['count'] = sum(total_outcome_counts.values())
        

        for outcome in outcome_records:
            product_name = outcome.product.name
            count = outcome.count
            date = outcome.date
            total = outcome.total
            transactions['outcome'][product_name] = {
                'count': count,
                'date': date,
                'total': total,
            }

        for income in income_records:
            product_name = income.product.name
            count = income.count
            date = income.date
            total = income.total
            transactions['income'][product_name] = {
                'count': count,
                'date': date,
                'total': total,
            }

            # Update total_income directly in debt_counts
            transactions['debt_counts'][product_name] = {
                'count': total_outcome_counts.get(product_name, 0) - total_income_counts.get(product_name, 0),
                'total': total_outcome_amounts.get(product_name, 0) - total_income_amounts.get(product_name, 0),
                'status': "",  # Update this based on your requirements
            }

        for product_name in set(transactions['outcome'].keys()) | set(transactions['income'].keys()):
            outcome_info = transactions['outcome'].get(product_name, {'count': 0, 'date': None, 'total': 0})
            income_info = transactions['income'].get(product_name, {'count': 0, 'date': None, 'total': 0})

            outcome_count = outcome_info['count']
            income_count = total_income_counts.get(product_name, 0)
            product_debt_count = outcome_count - income_count
            transactions['debt_counts'][product_name]['count'] = product_debt_count

            # Check if both count and total are 0
            if product_debt_count == 0 and transactions['debt_counts'][product_name]['total'] == 0:
                transactions['debt_counts'][product_name]['status'] = "Shartnoma yakunlangan"
            else:
                transactions['debt_counts'][product_name]['status'] = "Qarzdorlik"

        return transactions



        
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
        return f"{self.client_name} , {self.product.name}"

    
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
        return f"{self.client.name} , {self.product.name}"
# class Income(models.Model):
#     rent = models.ForeignKey(Rent, on_delete=models.CASCADE)
#     client = models.ForeignKey(Client, on_delete=models.CASCADE)
#     product = models.ForeignKey(ProductType, on_delete=models.CASCADE)
#     count = models.PositiveBigIntegerField()
#     day = models.IntegerField()
#     date = models.DateTimeField()
    
#     @property
#     def client_name(self):
#         return self.client.name
    
#     @property
#     def rent_name(self):
#         return self.rent.client_name
    
#     @property
#     def product_name(self):
#         return self.product.name
    
    
#     @property
#     def total(self):
#         if self.price is not None and self.price > 0:
#             return self.price * self.count
#         elif self.product.price is not None:
#             return self.product.price * self.count
#         else:
#             return 0
#     # @property
#     # def debt_days(self):
#     #     today = timezone.localdate()
#     #     days_overdue = (today - ).days
#     #     return today
#     # def __str__(self):
#     #     return f"{self.client.name} , {self.product.name}"
