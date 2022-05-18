from atexit import register
from django.contrib import admin
from .models import Developer, Game, Customer, Transaksi, Review
# fariduri dongkrakKodok29
# Register your models here.
admin.site.register(Developer)
admin.site.register(Game)
admin.site.register(Transaksi)
admin.site.register(Review)
admin.site.register(Customer)