from django.db import models
from .base import TimeStampedModel
from .master import Resident

class SupportPlan(TimeStampedModel):
    resident = models.ForeignKey(Resident, on_delete=models.PROTECT, related_name='support_plans')

    class Meta:
        db_table = 'support_plan'
        verbose_name = '個別支援計画マスタ'
        verbose_name_plural = '5. 個別支援計画マスタ'

class SupportPlanRevision(TimeStampedModel):
    support_plan = models.ForeignKey(SupportPlan, on_delete=models.PROTECT, related_name='revisions')
    revision_no = models.PositiveIntegerField(verbose_name='リビジョン番号')
    plan_start_date = models.DateField(verbose_name='計画開始日')
    plan_end_date = models.DateField(verbose_name='計画終了日')
    is_active = models.BooleanField(default=True, verbose_name='有効フラグ')

    class Meta:
        db_table = 'support_plan_revision'
        verbose_name = '支援計画書（更新履歴）'
        verbose_name_plural = '6. 支援計画書（更新履歴）'
        unique_together = ('support_plan', 'revision_no')