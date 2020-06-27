from django import forms
from database.models import Asset


class AddAssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'code', 'total_amount', 'desc']
        labels = {'name': 'Asset Name', 'total_amount': 'Total Amount', 'desc': 'Description'}
        widgets = {'desc': forms.Textarea()}
