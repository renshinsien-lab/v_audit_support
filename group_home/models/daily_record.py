# group_home/models/daily_record.py
from django.db import models
from django.utils import timezone
from .master import Resident

class DailyRecord(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='daily_records')
    record_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'daily_record'
        unique_together = ('resident', 'record_date')

class DailyRecordItem(models.Model):
    daily_record = models.ForeignKey(DailyRecord, on_delete=models.CASCADE, related_name='items')
    target_goal_no = models.IntegerField(null=True, blank=True)
    item_value = models.TextField()
    
    # --- バイタル項目を追加 ---
    body_temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="体温")
    blood_pressure_high = models.IntegerField(null=True, blank=True, verbose_name="血圧(高)")
    blood_pressure_low = models.IntegerField(null=True, blank=True, verbose_name="血圧(低)")
    pulse = models.IntegerField(null=True, blank=True, verbose_name="脈拍")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'daily_record_item'