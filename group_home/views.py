# group_home/views.py
import json
import calendar
from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from .forms import DailyRecordForm, DailyRecordItemForm

# モデルのインポート
from .models import (
    Resident, DailyRecord, DailyRecordItem, 
    # SupportPlanRevision, SupportPlanGoal, SupportPlanContent, Monitoring
     SupportPlanRevision, SupportPlanGoal, SupportPlanContent, Monitoring
)

# --- 1. 利用者一覧 ---
def resident_list_view(request):
    residents = Resident.objects.all()
    now = timezone.now()
    
    # 各利用者の今月の記録状況を確認（バッジ用）
    for resident in residents:
        has_records = DailyRecordItem.objects.filter(
            daily_record__resident=resident,
            daily_record__record_date__year=now.year,
            daily_record__record_date__month=now.month,
            target_goal_no__isnull=False
        ).exists()
        resident.monitoring_ready = has_records

    return render(request, 'group_home/resident_list.html', {
        'residents': residents,
        'this_year': now.year,
        'this_month': now.month,
    })

# --- 2. 日報入力（スマホ・音声・AI・定型文対応） ---
# group_home/views.py の daily_record_form_view を差し替え

def daily_record_form_view(request, resident_id):
    resident = get_object_or_404(Resident, pk=resident_id)
    
    if request.method == "POST":
        goal_no = request.POST.get('target_goal_no')
        content = request.POST.get('item_value')
        
        # バイタル値の取得（空文字の場合は None にする）
        def get_val(key):
            val = request.POST.get(key)
            return val if val else None

        # 今日付のDailyRecordを取得または作成
        record, _ = DailyRecord.objects.get_or_create(
            resident=resident,
            record_date=timezone.now().date()
        )
        
        # 記録明細とバイタルを保存
        DailyRecordItem.objects.create(
            daily_record=record,
            target_goal_no=goal_no if goal_no else None,
            item_value=content,
            body_temperature=get_val('body_temperature'),
            blood_pressure_high=get_val('blood_pressure_high'),
            blood_pressure_low=get_val('blood_pressure_low'),
            pulse=get_val('pulse'),
        )
        return redirect('resident_list')

    return render(request, 'group_home/daily_record_form.html', {'resident': resident})
# --- 3. AI整形API ---
@require_POST
def ai_format_api(request):
    """話し言葉を専門用語に擬似整形する"""
    try:
        data = json.loads(request.body)
        raw_text = data.get('text', '')
        # 今後Gemini API等に置き換え可能な部分
        formatted_text = f"【支援経過】\n{raw_text}\n\n意向を尊重した支援を実施。特段の異常なし。継続して経過を観察する。"
        return JsonResponse({'formatted_text': formatted_text})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# --- 4. モニタリング報告書 ---
def monitoring_report_view(request, resident_id, year, month):
    resident = get_object_or_404(Resident, pk=resident_id)
    
    last_day = calendar.monthrange(year, month)[1]
    start_date = date(year, month, 1)
    end_date = date(year, month, last_day)

    daily_items = DailyRecordItem.objects.filter(
        daily_record__resident=resident,
        daily_record__record_date__range=[start_date, end_date],
        target_goal_no__isnull=False
    ).select_related('daily_record')

    summary = {}
    for item in daily_items:
        g_no = item.target_goal_no
        if g_no not in summary:
            summary[g_no] = []
        summary[g_no].append(item)

    return render(request, 'group_home/monitoring_report.html', {
        'resident': resident,
        'year': year,
        'month': month,
        'summary': summary,
    })

# --- 5. 監査ログ ---
def audit_log_view(request, resident_id):
    """監査証跡としての時系列記録を表示"""
    resident = get_object_or_404(Resident, pk=resident_id)
    records = DailyRecordItem.objects.filter(
        daily_record__resident=resident
    ).select_related('daily_record').order_by('-daily_record__record_date')
    
    return render(request, 'group_home/audit_log.html', {
        'resident': resident,
        'records': records,
    })

# --- 6. 計画確定などの補助機能 ---
def finalize_revision(request, revision_id):
    if request.method == 'POST':
        rev = get_object_or_404(SupportPlanRevision, pk=revision_id)
        SupportPlanRevision.objects.filter(support_plan=rev.support_plan, status='agreed').update(status='expired')
        rev.status = 'agreed'
        rev.agreed_at = request.POST.get('agreed_at')
        rev.save()
    return redirect('audit_log', resident_id=rev.support_plan.resident.id)

def daily_record_create(request, resident_id):
    resident = get_object_or_404(Resident, id=resident_id)
    
    if request.method == 'POST':
        # 保存処理...
        pass
    else:
        form = DailyRecordForm()
        
    return render(request, 'group_home/daily_record_form.html', {
        'form': form,
        'resident': resident, # これがグラフ表示に必須
    })

def vital_graph_data(request, resident_id):
    # 直近30日分などのデータを取得
    items = DailyRecordItem.objects.filter(
        daily_record__resident_id=resident_id
    ).select_related('daily_record').order_by('-daily_record__record_date')[:30]

    # グラフ用に日付の昇順に並び替え
    items = reversed(items)

    data = {
        'labels': [item.daily_record.record_date.strftime('%m/%d') for item in items],
        'temp': [float(item.body_temperature) if item.body_temperature else None for item in items],
        'bp_high': [item.blood_pressure_high for item in items],
        'bp_low': [item.blood_pressure_low for item in items],
        'pulse': [item.pulse for item in items],
    }
    return JsonResponse(data)