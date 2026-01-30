from django.db import models
from .base import TimeStampedModel
from .plan import SupportPlanRevision

class Monitoring(TimeStampedModel):
    """
    支援計画の実施状況を評価（モニタリング）するモデル
    """
    ACHIEVEMENT_CHOICES = [
        ('A', '達成（継続）'),
        ('B', '一部達成（内容変更）'),
        ('C', '未達成（計画見直し）'),
        ('D', '目標消滅'),
    ]

    support_plan_revision = models.ForeignKey(
        SupportPlanRevision, 
        on_delete=models.PROTECT, 
        related_name='monitorings',
        verbose_name='対象計画リビジョン'
    )
    target_goal_no = models.PositiveIntegerField(verbose_name='対象目標番号')
    monitoring_date = models.DateField(verbose_name='モニタリング実施日')
    achievement_status = models.CharField(
        max_length=1, 
        choices=ACHIEVEMENT_CHOICES, 
        verbose_name='進捗評価'
    )
    comment = models.TextField(verbose_name='評価コメント・特記事項')

    class Meta:
        db_table = 'monitoring'
        verbose_name = 'モニタリング'
        verbose_name_plural = 'モニタリング'

    def __str__(self):
        return f"{self.monitoring_date} - 目標{self.target_goal_no}"
