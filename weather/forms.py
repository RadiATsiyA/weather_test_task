from django import forms


class CityForm(forms.Form):
    city = forms.CharField(label="city", max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-class',
        'placeholder': 'Выберите город',
        'id': 'inputName',
    }))
