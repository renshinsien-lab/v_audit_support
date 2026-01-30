from django.db import models
from .base import TimeStampedModel
from .master import Resident, Office

class DailyRecord(TimeStampedModel):
    resident = models.ForeignKey(Resident, on_delete=models.PROTECT, related_name='daily_records')
    office = models.ForeignKey(Office, on_delete=models.PROTECT, related_name='daily_records')
    record_date = models.DateField(verbose_name='記録日')

    class Meta:
        db_table = 'daily_record'
        unique_together = ('resident', 'office', 'record_date')

        verbose_name = '日次記録'
        verbose_name_plural = '7. サービス実施記録'

class DailyRecordItem(TimeStampedModel):
    daily_record = models.ForeignKey(
        DailyRecord, on_delete=models.CASCADE, related_name='items'
    )
    # 監査対応: どの目標に基づく支援かを選択可能にする
    target_goal_no = models.PositiveIntegerField(
        verbose_name='対象目標番号', 
        help_text='計画書の「目標番号」を入力',
        null=True, blank=True
    )
    item_code = models.CharField(max_length=50, verbose_name='項目コード')
    item_value = models.TextField(verbose_name='実施内容・結果')

    class Meta:
        db_table = 'daily_record_item'
        verbose_name = '実施詳細'
        verbose_name_plural = '実施詳細'