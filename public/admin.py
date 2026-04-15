from django.contrib import admin
from public.models import User
from public.models import CustomUser
from public.models import Category
from public.models import Equipment
from public.models import Rent
from public.models import Withdraw
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Equipment)
admin.site.register(Rent)
admin.site.register(Withdraw)
