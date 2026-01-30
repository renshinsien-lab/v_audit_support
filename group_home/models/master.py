from django.db import models
from .base import TimeStampedModel

class Company(TimeStampedModel):
    company_code = models.CharField(max_length=20, unique=True, verbose_name='法人コード')
    name = models.CharField(max_length=255, verbose_name='法人名')
    is_active = models.BooleanField(default=True, verbose_name='有効フラグ')

    def __str__(self): return self.name
    
    class Meta:
        db_table = 'company'
        verbose_name = '1. 法人'
        verbose_name_plural = '1. 法人管理'

class Office(TimeStampedModel):
    office_code = models.CharField(max_length=20, unique=True, verbose_name='事業所コード')
    company = models.ForeignKey(Company, on_delete=models.PROTECT, related_name='offices')
    name = models.CharField(max_length=255, verbose_name='事業所名')
    opened_on = models.DateField(verbose_name='開設日')
    closed_on = models.DateField(null=True, blank=True, verbose_name='廃止日')

    def __str__(self): return self.name
    
    class Meta:
        db_table = 'office'
        verbose_name = '2. 事業所'
        verbose_name_plural = '2. 事業所管理'

class Resident(TimeStampedModel):
    resident_code = models.CharField(max_length=20, unique=True, verbose_name='利用者コード')
    name = models.CharField(max_length=255, verbose_name='利用者名')
    birth_date = models.DateField(verbose_name='生年月日')

    def __str__(self): return self.name
    
    class Meta:
        db_table = 'resident'
        verbose_name = '3. 利用者'
        verbose_name_plural = '3. 利用者マスタ'
