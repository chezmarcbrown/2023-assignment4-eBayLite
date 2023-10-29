from django import forms
from .models import AuctionListing, Category

class AuctionListingForm(forms.ModelForm):

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select a Category (optional)", 
        widget=forms.Select(attrs={
            'class': 'form-control form-group',
        }
        )
    )

    class Meta:
        model = AuctionListing
        fields = ['title', 'description', 'price', 'starting_bid', 'category', 'image_url']  # add all the fields you want from your model
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control form-group',
                'placeholder': 'Give it a title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control form-group',
                'placeholder': 'Tell more about the product',
                'rows': '3'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control form-group',
                'placeholder': 'Estimated price (optional)',
                'min': '0.01',
                'max': '999999999.99',
                'step': '0.01'
            }),
            'starting_bid': forms.NumberInput(attrs={
                'class': 'form-control form-group',
                'placeholder': 'Starting bid',
                'min': '0.01',
                'max': '99999999999.99',
                'step': '0.01'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control form-group',
            }),
            'image_url': forms.FileInput(attrs={
                'class': 'form-control form-group',
            }),
        }

    def clean_starting_bid(self):
        amount = float(self.cleaned_data.get('starting_bid'))
        if isinstance(amount, float) and amount > 0:
            return amount
        print(amount)
        raise forms.ValidationError('Should be a number larger than zero!')

class CommentForm(forms.Form):
    text = forms.CharField(
        label='',
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control-md lead form-group',
            'rows': '3',
            'cols': '100'
        }
        )
    )

    def clean_comment(self):
        text = self.cleaned_data.get('text')
        if len(text) > 0:
            return text
        return self.errors
