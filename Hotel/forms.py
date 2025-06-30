from django import forms


class SearchForm(forms.Form):
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'City'
        })
    )
    check_in = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': 'Check in'
        })
    )
    check_out = forms.DateField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': 'Check out'
        })
    )
    adults = forms.IntegerField(
        min_value=1, initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adults'
        })
    )
    children = forms.IntegerField(
        min_value=0, initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kids'
        })
    )
    rooms = forms.IntegerField(
        min_value=1, initial=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rooms'
        })
    )