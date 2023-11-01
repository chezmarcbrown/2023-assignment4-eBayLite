from django import forms
from .models import Auction

class listingForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ["title", "description", "starting_price", "imageURL", "category"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "Enter the title", 
                       "class": "form-control"}),
            "description": forms.Textarea(
                attrs={"placeholder": "Enter the item description", 
                       "class": "form-control", 
                       "rows": 10}),
            "starting_price": forms.NumberInput(
                attrs={"class": "form-control"}),
            "imageURL": forms.URLInput(
                attrs={"placeholder": "Enter the image URL", 
                       "class": "form-control"})
        }