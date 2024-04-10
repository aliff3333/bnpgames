from django import forms

from .models import Review


class ReviewForm(forms.Form):
    RATING_CHOICES = ((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'),)

    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                        'rows': 4,
                                                        'placeholder': 'متن بررسی'}))
    rating = forms.ChoiceField(choices=RATING_CHOICES, label='امتیاز')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs['class'] = 'form-control'
