from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(ProductType)


class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "phone",
    ]
    list_per_page = 10

    class Meta:
        model = Client


admin.site.register(Client, ClientAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_per_page = 10

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)


class OutcomeInline(admin.TabularInline):
    model = Outcome
    fields = ["client", "product", "count", "date"]


admin.site.register(Outcome)


class IncomeInline(admin.TabularInline):
    model = Income
    fields = ["client", "product", "count", "day", "date"]


admin.site.register(Income)


class PaymentsAdmin(admin.ModelAdmin):
    list_display = ["client", "summa", "date"]
    list_per_page = 10

    class Meta:
        model = Payments


admin.site.register(Payments, PaymentsAdmin)
