from django import forms


class BookingForm(forms.Form):
    check_in = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    check_out = forms.DateField(
        input_formats=['%d-%m-%Y'],
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )

    def clean(self):
        cleaned = super().clean()
        ci, co = cleaned.get('check_in'), cleaned.get('check_out')
        if ci and co and ci >= co:
            raise forms.ValidationError("Check out should be later.")
        return cleaned