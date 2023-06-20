from django import forms
from order.models import Order


class Place_Order_Form(forms.ModelForm):
    """ Form for place order """
    class Meta:
        model = Order
        fields = ['mobile', 'address']

    def __init__(self, *args, **kwargs):
        super(Place_Order_Form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'