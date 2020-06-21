from django import forms
from database.models import Products


class OrderQuantityForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OrderQuantityForm, self).__init__(*args, **kwargs)
        products = Products.objects.all()
        for product in products:
            self.fields['%s' % product.code] = forms.IntegerField(label='%s quantity' % product.name,
                                                                  required=True, initial=0)


class OrderForm(forms.Form):
    address = forms.CharField(max_length=300, label='Address (leave blank for your default address)', required=False)
    order_types = [(1, 'Once only'), (2, 'Recursive')]
    order_type = forms.ChoiceField(choices=order_types, initial=1, label='Order type')
