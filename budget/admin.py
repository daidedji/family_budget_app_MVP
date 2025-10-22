from django.contrib import admin
from .models import User, Funds, Debt, Transaction, Budget, FamilyRelation, Bill

admin.site.register(User)
admin.site.register(Funds)
admin.site.register(Debt)
admin.site.register(Transaction)
admin.site.register(Budget)
admin.site.register(FamilyRelation)
admin.site.register(Bill)
