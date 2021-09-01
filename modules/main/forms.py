from django import forms

from modules.main.models import Messages


class MessageForm(forms.ModelForm):
    mess = forms.CharField(
        label = 'Wiadomość',
        widget=forms.Textarea(
            attrs={
                "placeholder": "Wpisz wiadomość",
                "class": "form-control",
                'autocomplete': 'new-password',
                'rows': 5,
                'cols': 15,
            }
        )
    )
    class Meta:
        model = Messages
        fields = ['mess']
