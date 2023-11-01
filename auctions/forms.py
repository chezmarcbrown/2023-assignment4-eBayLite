from django import forms
from .models import Auction, Watchlist, Bid, Category, Comment

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

class biddingForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ["bid_price"]

class commentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["headline", "message"]
        widgets = {
            "headline": forms.TextInput(
                attrs={"placeholder": "Enter title",
                       "class": "form-control"
            }),
            "message": forms.Textarea(
                attrs={"placeholder": "Enter your comment...",
                       "class": "form-control",
                       "rows": 4
            })
        }        