from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

from .models import Auction, Bid, Category, Comment, User
from .forms import AuctionForm, CommentForm



def index(request):
    return render(request, "auctions/index.html", {
        "auctions" : Auction.objects.all().order_by('-time'),
        "user" : request.user
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

def create(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.user = request.user
            auction.save()

            bid = Bid(user=request.user, auction=auction, bid=auction.current_bid)
            bid.save()
            return  HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/create.html", {
        "form" : AuctionForm()
            })
    return render(request, "auctions/create.html", {
        "form" : AuctionForm()
    })

def auction(request, auction_id):
    #WRONG: auction = AuctionForm.objects.get(pk=auction_id)
    auction = get_object_or_404(Auction, id=auction_id)
    return render(request, "auctions/auction.html", {
        'auction' : auction,
        'user' : request.user,
        'bid' : get_object_or_404(Bid, auction=auction),
        'comments' : Comment.objects.filter(auction=auction),
        'comment_form' : CommentForm()
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        'categories' : Category.objects.all()
    })

def filterCategories(request, category):
    # The fact that Django does not give a foreign key as a string when it is assigned as a string is infuriating

    list = []
    for object in Auction.objects.all():
        if(str(object.category).strip() == category):
            list.append(object)

    if list:
        auction = list
    else:
        auction = Auction.objects.all()
    return render(request, "auctions/category.html", {
        'auctions' : auction,
        'name' : category
    })

@login_required(login_url="login")
def watchlist(request):
    # URL gets super wierdly formatted here when having a login be required. I don't know how to fix it.
    return render(request, "auctions/watchlist.html", {
        'watchlist' : request.user.watchlist.all()
    })

@login_required(login_url="login")
def watch(request, auction_id):
    # Untested Code
    request.user.watchlist.add(get_object_or_404(Auction, id=auction_id))
    request.user.save()
    return HttpResponseRedirect(reverse('auctions:watchlist'))

@login_required(login_url="login")
def unwatch(request, auction_id):
    # Untested Code
    request.user.watchlist.remove(get_object_or_404(Auction, id=auction_id))
    request.user.save()
    return HttpResponseRedirect(reverse('auctions:watchlist'))

@login_required(login_url="login")
def updatebid(request, auction_id):
    pass
    
@login_required(login_url="login")
def closebid(request, auction_id):
    pass

@login_required(login_url="login")
def comment(request, auction_id):
    pass