from django.db import models
from .master import Resident, Office
from .base import TimeStampedModel

class ResidentOffice(TimeStampedModel):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='offices', verbose_name='利用者')
    office = models.ForeignKey(Office, on_delete=models.CASCADE, related_name='residents', verbose_name='事業所')
    
    # ここを start_date, end_date に統一します
    start_date = models.DateField(verbose_name='利用開始日') 
    end_date = models.DateField(null=True, blank=True, verbose_name='利用終了日')

    class Meta:
        db_table = 'resident_office'
        verbose_name = '利用者在籍履歴'
        verbose_name_plural = '4. 利用者在籍・契約管理'

    def __str__(self):
        return f"{self.resident.name} - {self.office.name}"