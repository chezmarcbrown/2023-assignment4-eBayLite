from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Auction, User, Bid, Comment
from .forms import AuctionForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError



def index(request):
    return render(request, "auctions/index.html", {
        "auctions":Auction.objects.all(),
        "user": request.user
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
    if request.method == "POST":
        f = AuctionForm(request.POST)
        if f.is_valid():
            auction = Auction(user=request.user, **f.cleaned_data)
            auction.save()
            price  = auction.price
            bid = Bid(user=request.user, auction=auction, bid=price)
            bid.save()
            return HttpResponseRedirect(reverse('auctions:index'))
        else:
            return render(request, 'auctions/create_listing.html', {
                'form': f
            })
    return render(request, "auctions/create_listing.html", {
        "form": AuctionForm()
    })

def auction(request, auction_id):# show the auction you click on
    auction = get_object_or_404(Auction, id=auction_id)
    bid = get_object_or_404(Bid, auction=auction)
    comments = Comment.objects.filter(auction=auction)
    return render(request, "auctions/auction.html", {
        'auction': auction,
        "bid": bid,
        "user": request.user,
        "comments": comments,
        "commentform": CommentForm
    })

def categories(request):#show a list of all categories and be able to select on and go to category
    categories = Auction.CATEGORIES
    categories_fixed = []
    for x in categories:
        categories_fixed.append(x[1])
    return render(request, "auctions/categories.html", {
        'categories': categories_fixed
    })

def category(request, cat_name):# show a list of all auctions within the category you selected
    auctions = Auction.objects.filter(category=cat_name)
    return render(request, "auctions/category.html", {
        'auctions': auctions,
        "name": cat_name
    })

@login_required(login_url='auctions/login.html')
def wishlist(request):
    return render(request, "auctions/wishlist.html", {
        'wishlist': request.user.wishlist.all()# displays all on wishlist
    })

@login_required(login_url='auctions/login.html')
def addwishlist(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    request.user.wishlist.add(auction)# adds to the wishlist stored in User
    request.user.save()# saves to database
    return HttpResponseRedirect(reverse("auctions:wishlist"))

@login_required(login_url='auctions/login.html')
def removewishlist(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    request.user.wishlist.remove(auction)
    request.user.save()
    return HttpResponseRedirect(reverse("auctions:wishlist"))

@login_required(login_url='auctions/login.html')
def makebid(request, bid_id, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    price = request.POST['bid']# gets input from form in auction.html
    if price != None:
        price = float(price)
        if price > get_object_or_404(Bid, id=bid_id).bid:
            bid = get_object_or_404(Bid, id=bid_id)
            bid.user = request.user
            bid.bid = price
            #bid.auction.price = price
            bid.save()
            auction.price = price
            auction.save()
            #addwishlist(request, auction_id)
            return HttpResponseRedirect(reverse('auctions:index'))
        else:
            raise ValueError('Bid needs to be larger than current highest bid')  
        
@login_required(login_url='auctions/login.html')
def comment(request, auction_id):
    auction = get_object_or_404(Auction, id=auction_id)
    if request.method == "POST":
        f = CommentForm(request.POST)
        if f.is_valid():
            text = f.cleaned_data
            comment = Comment(user=request.user,auction=auction, **text)
            comment.save()
            return HttpResponseRedirect(reverse('auctions:index'))

@login_required(login_url='auctions/login.html')
def closebid(request, auction_id):
    #close the auction
    auction = get_object_or_404(Auction, id=auction_id)#get auction object
    auction.winner = request.user.username# save highest bidder as the winner
    auction.closed = True# close the auction
    auction.save()# save to the database
    return HttpResponseRedirect(reverse('auctions:index'))