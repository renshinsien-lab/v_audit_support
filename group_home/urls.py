from django.urls import path
from . import views

urlpatterns = [
    # 既存のパス
    path('residents/', views.resident_list_view, name='resident_list'),
    # この 'name' の部分がテンプレートの {% url '...' %} と一致する必要があります
    path('monitoring/<int:resident_id>/<int:year>/<int:month>/', 
         views.monitoring_report_view, 
         name='monitoring_report_view'), # ここを追加・確認
    
    path('audit/<int:resident_id>/', views.audit_log_view, name='audit_log'),
    path('finalize/<int:revision_id>/', views.finalize_revision, name='finalize_revision'),
    # 日報入力のURL名
    path('daily-record/<int:resident_id>/add/', 
         views.daily_record_create, 
         name='daily_record_create'),
    
    # --- ここから不足分を追加 ---
    path('record/add/<int:resident_id>/', views.daily_record_form_view, name='daily_record_add'),
    path('ai-format-api/', views.ai_format_api, name='ai_format_api'),
    # グラフデータ取得用API
    path('api/vital-graph/<int:resident_id>/', views.vital_graph_data, name='vital_graph_data'),
]