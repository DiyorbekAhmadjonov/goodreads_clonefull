from django import forms

from books.models import BookReview


class BookReviewForm(forms.ModelForm):
    # stars_given = forms.IntegerField(min_value=1, max_value=5)
    stars_given = forms.ChoiceField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
        
    class Meta:
        model = BookReview
        fields = ['stars_given', 'comment']
    
        
        # widgets = {
        #     'stars_given': forms.NumberInput(attrs={'class': 'form-control'}),
        # }
