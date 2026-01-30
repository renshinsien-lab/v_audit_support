from django import forms
from .models import DailyRecord, DailyRecordItem

class DailyRecordForm(forms.ModelForm):
    """日報の基本情報（日付など）用フォーム"""
    class Meta:
        model = DailyRecord
        fields = ['record_date']
        widgets = {
            'record_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class DailyRecordItemForm(forms.ModelForm):
    """バイタル項目を含む日報明細用フォーム"""
    class Meta:
        model = DailyRecordItem
        fields = [
            'target_goal_no', 
            'item_value', 
            'body_temperature', 
            'blood_pressure_high', 
            'blood_pressure_low', 
            'pulse'
        ]
        widgets = {
            'target_goal_no': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '目標番号'}),
            'item_value': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': '実施内容・様子'}),
            'body_temperature': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': '36.5'}),
            'blood_pressure_high': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '120'}),
            'blood_pressure_low': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '80'}),
            'pulse': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '70'}),
        }
