from django.db import models
from django.forms import ValidationError


class City(models.Model):
    name = models.CharField(max_length=64, verbose_name='name')

    class Meta:
        verbose_name = 'city'
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name


class Street(models.Model):
    name = models.CharField(max_length=128, verbose_name='name')
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name='city')

    class Meta:
        verbose_name = 'street'
        verbose_name_plural = 'streets'

    def __str__(self):
        return self.name


class Shop(models.Model):
    name = models.CharField(max_length=128, verbose_name='name')
    city = models.ForeignKey('City', on_delete=models.PROTECT, verbose_name='city')
    street = models.ForeignKey('Street', on_delete=models.PROTECT, verbose_name='street')
    building = models.PositiveIntegerField(verbose_name='building')
    opening_time = models.TimeField(verbose_name='opening_time')
    closing_time = models.TimeField(verbose_name='closing_time')

    def clean(self):
        super().clean()
        if self.street.city != self.city:
            raise ValidationError('The street does not belong to the selected city.')

    class Meta:
        verbose_name = 'shop'
        verbose_name_plural = 'shops'
        unique_together = ('name', 'city', 'street', 'building')

    def __str__(self):
        return self.name
