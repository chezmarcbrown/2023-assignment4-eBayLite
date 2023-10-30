# ---------------------------------------------------------------------------------------
# This code was developed with assistance from the following:
# - Django Documentation: https://docs.djangoproject.com/en/4.2/topics/forms/modelforms/
# - Assisted by OpenAI's ChatGPT for additional guidance and debugging
#
# ----------------------------------------------------------------------------------------

from django import forms
from .models import AuctionListing, Category, Bid, Comment 

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

class AuctionForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
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

