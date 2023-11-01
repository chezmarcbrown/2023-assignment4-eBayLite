from django import forms
from .models import Auction, Category

class AuctionForm(forms.ModelForm):
    

    class Meta:
        model = Auction
        fields=['title', 'description', 'current_bid', 'category','image_url']

        title = forms.CharField(
            label='Title',
            required=True,
            widget=forms.TextInput(attrs={
                'class': 'form-control form-group',
                'placeholder': "Please Enter a Title"
            })
        )
        description = forms.CharField(
            label='Description',
            required=True,
            widget=forms.Textarea(attrs={
                'class' : 'form-control form-group',
                'placeholder' : "Please Enter a Description",
                'rows' : '3'
            })
        )
        current_bid = forms.DecimalField(
            label='Price',
            required=False,
            initial=0.0,
            widget=forms.NumberInput(attrs={
                'class' : 'form-control form-group',
                'placeholder' : "Starting Bid",
                'min' : '0.01',
                'max' : '99999999.99',
                'step': '0.01'
            })
        )
        category = forms.ModelChoiceField(
            label='Category',
            required=False,
            queryset=Category.objects.all(),
            widget=forms.Select(attrs={
                'class' : 'form-control form-group',
                'placeholder' : "Category",
                'autocomplete' : 'on'
            })
        )
        image_url = forms.URLField(
            label='Image URL',
            required=False,
            initial='',
            widget=forms.TextInput(attrs={
            'class' : 'form-control form-group',
            'placeholder' : "Optional Image URL"
            })
        )
    

class CommentForm(forms.Form):
    comment = forms.CharField(
        label='Comment',
        required=True,
        widget=forms.Textarea(attrs={
            'class' : 'form-control form-group',
            'placeholder' : "Comment Here",
            'rows' : '3'
        })
    )
