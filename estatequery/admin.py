from django.contrib import admin
from .models import RealEstate
# Register your models here.
class RealEstateAdmin(admin.ModelAdmin):
    list_display = ("price", "created_at",)

admin.site.register(RealEstate, RealEstateAdmin)