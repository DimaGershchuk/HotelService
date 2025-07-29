from django import forms
from .models import HotelReview


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
        input_formats=['%d-%m-%Y'],
        widget=forms.TextInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': 'Check in'
        })
    )
    check_out = forms.DateField(
        required=False,
        input_formats=['%d-%m-%Y'],
        widget=forms.TextInput(attrs={
            'class': 'form-control datepicker',
            'placeholder': 'Check out'
        })
    )

    min_price = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'From ₴'
    }))
    max_price = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control', 'placeholder': 'to ₴'
    }))

    adults = forms.IntegerField(
        min_value=1, initial=1, required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Adults'
        })
    )
    
    rooms = forms.IntegerField(
        min_value=1, initial=1,required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rooms'
        })
    )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = HotelReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, '★' * i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }