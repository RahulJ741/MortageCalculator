from django import forms

class MortageForm(forms.Form):
    loan_amnt = forms.IntegerField(label="Loan Amount")
    rate_of_intrest = forms.IntegerField(label="Rate of Intrest")
    loan_months = forms.IntegerField(label="Loan Months")

    def __init__(self, *args, **kwargs):
        super(MortageForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
