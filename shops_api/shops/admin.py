from django.contrib import admin

from shops_api.shops.models import Shop, City, Street


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    """
    Shop model class for django admin site
    """
    list_display = ('id', 'name', 'city', 'street', 'building', 'opening_time', 'closing_time')
    search_fields = ('name', 'city', 'street', 'building')
    list_filter = (
        ('city', admin.RelatedOnlyFieldListFilter),
        ('street', admin.RelatedOnlyFieldListFilter),
        ('opening_time', admin.DateFieldListFilter),
        ('closing_time', admin.BooleanFieldListFilter),
    )


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """
    City model class for django admin site
    """
    list_display = ('id', 'name')
    search_fields = ('name',)



@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    """
    Street model class for django admin site
    """
    list_display = ('id', 'name', 'city')
    search_fields = ('name', 'city')
    list_filter = (
        ('city', admin.RelatedOnlyFieldListFilter),
        )
