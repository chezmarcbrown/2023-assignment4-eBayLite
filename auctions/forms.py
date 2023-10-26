from django import forms
from .models import AuctionListing, Category, Bid, Comment 

class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ('name',)

class AuctionForm(forms.ModelForm):
    
    class Meta:
        model = AuctionListing
        fields = ('title', 'description', 'starting_bid', 'image_url', 'category', 'active')
        
class BidForm(forms.ModelForm):
    
    class Meta:
        model = Bid
        fields = ('amount',)
        
class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment
        fields = ('content',)

