from django.contrib import admin
from .models import Developer, Game, Customer, Transaction, Review, Genre, Profile

admin.site.register(Profile)
admin.site.register(Developer)
admin.site.register(Game)
admin.site.register(Transaction)
admin.site.register(Review)
admin.site.register(Customer)
admin.site.register(Genre)

# fariduri makassar25