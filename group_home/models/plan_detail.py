from django.db import models
from .base import TimeStampedModel
from .plan import SupportPlanRevision

class SupportPlanGoal(TimeStampedModel):
    support_plan_revision = models.ForeignKey(SupportPlanRevision, on_delete=models.PROTECT, related_name='goals')
    goal_no = models.PositiveIntegerField(verbose_name='目標番号')
    goal_text = models.TextField(verbose_name='目標内容')

    class Meta:
        db_table = 'support_plan_goal'
        unique_together = ('support_plan_revision', 'goal_no')

        verbose_name = '支援計画'
        verbose_name_plural = '5. 支援計画（基本）'

class SupportPlanContent(TimeStampedModel):
    support_plan_revision = models.ForeignKey(SupportPlanRevision, on_delete=models.PROTECT, related_name='contents')
    content_no = models.PositiveIntegerField(verbose_name='支援内容番号')
    content_text = models.TextField(verbose_name='支援内容')
    related_goal_no = models.PositiveIntegerField(null=True, blank=True, verbose_name='対応目標番号')

    class Meta:
        db_table = 'support_plan_content'
        unique_together = ('support_plan_revision', 'content_no')
        
        verbose_name = '計画リビジョン'
        verbose_name_plural = '6. 計画作成・更新履歴'
