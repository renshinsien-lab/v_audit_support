from django.contrib import admin
from django import forms
from .models import (
    Resident, Company, Office, ResidentOffice,
    DailyRecord, DailyRecordItem,
    SupportPlan, SupportPlanRevision, SupportPlanGoal, SupportPlanContent,
    Monitoring
)

# --- 二重登録エラー (AlreadyRegistered) 回避策 ---
# サーバー再起動時の読み込み重複を防ぐため、登録済みの場合は一度解除します
models_to_reset = [DailyRecord, DailyRecordItem]
for model in models_to_reset:
    if admin.site.is_registered(model):
        admin.site.unregister(model)

# --- フォーム定義 ---
class DailyRecordItemForm(forms.ModelForm):
    """日報詳細の入力フォーム。バイタル項目を含みます。"""
    class Meta:
        model = DailyRecordItem
        fields = '__all__'
        widgets = {
            'item_value': forms.Textarea(attrs={'rows': 3}),
        }

# --- インライン設定 ---
class DailyRecordItemInline(admin.TabularInline):
    """日報画面の下部で、詳細レコード（バイタル含む）を直接編集できるようにします。"""
    model = DailyRecordItem
    form = DailyRecordItemForm
    extra = 1
    # 画面に並べる項目
    fields = [
        'target_goal_no', 'item_value', 
        'body_temperature', 'blood_pressure_high', 'blood_pressure_low', 'pulse'
    ]

class ResidentOfficeInline(admin.TabularInline):
    """利用者画面で事業所所属履歴を表示します。"""
    model = ResidentOffice
    extra = 1

# --- 各モデルの管理設定 ---

@admin.register(DailyRecord)
class DailyRecordAdmin(admin.ModelAdmin):
    """日報の管理設定。詳細（DailyRecordItem）をインラインで持ちます。"""
    list_display = ['resident', 'record_date', 'created_at']
    list_filter = ['record_date', 'resident']
    search_fields = ['resident__name']
    inlines = [DailyRecordItemInline]

@admin.register(DailyRecordItem)
class DailyRecordItemAdmin(admin.ModelAdmin):
    """詳細レコード単体での閲覧・修正用。"""
    list_display = [
        'get_resident', 'get_date', 'body_temperature', 
        'blood_pressure_high', 'blood_pressure_low', 'pulse'
    ]
    list_filter = ['daily_record__record_date']

    def get_resident(self, obj):
        return obj.daily_record.resident.name
    get_resident.short_description = '利用者名'

    def get_date(self, obj):
        return obj.daily_record.record_date
    get_date.short_description = '記録日'

@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
    list_display = ['name', 'resident_code', 'birth_date']
    search_fields = ['name', 'resident_code']
    inlines = [ResidentOfficeInline]

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'company_code', 'is_active']

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ['name', 'office_code', 'company']

@admin.register(ResidentOffice)
class ResidentOfficeAdmin(admin.ModelAdmin):
    list_display = ['resident', 'office', 'start_date', 'end_date']

# 計画・モニタリング関連の登録
@admin.register(SupportPlan)
class SupportPlanAdmin(admin.ModelAdmin):
    list_display = ['resident', 'created_at']

@admin.register(SupportPlanRevision)
class SupportPlanRevisionAdmin(admin.ModelAdmin):
    list_display = ['support_plan', 'revision_no', 'plan_start_date', 'is_active']

@admin.register(Monitoring)
class MonitoringAdmin(admin.ModelAdmin):
    list_display = ['monitoring_date', 'target_goal_no', 'achievement_status']