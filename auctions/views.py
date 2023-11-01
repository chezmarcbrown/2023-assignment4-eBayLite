from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count, Max
from django.contrib import messages

from .models import User, Auction, Category, Watchlist, Bid, Comment
from .forms import listingForm, biddingForm, commentForm


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    

@login_required(login_url = "login")    
def create(request):
    if request.method == 'POST':
        create_form = listingForm(request.POST, request.FILES)
        if create_form == 1:
            new_listing = create_form.save(commit=False)
            new_listing.starting_price = create_form.cleaned_data['starting_price']
            new_listing.save()

            return HttpResponseRedirect(reverse("index"))
        else:
            create_form = listingForm()
            return render(request, "auctions/create.html", 
                          {"form": create_form})
    
    if request.method == 'GET':
        create_form = listingForm()
        return render(request, "auctions/create.html", 
                      {"form": create_form})


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", 
                  {"categories": categories})


def category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    auctions = Auction.objects.filter(category=category, closed=False).order_by('-create_date')
    return render(request, "auctions/category.html", 
                  {"auctions": auctions, 
                   "category": category})


@login_required(login_url="login")
def watchlist(request):
    try:
        watchlist = Watchlist.objects.get_or_create(user=request.user)
        auctions = watchlist.auctions.all().order_by('-id')
        watchNum = watchlist.auctions.count()

    except ObjectDoesNotExist:
        watchlist = None
        auctions = None
        watchNum = 0

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "auctions": auctions,
        "watchNum": watchNum
    })


def listings(request, auction_id):
    try:
        auction = Auction.objects.get(pk=auction_id)
    except Auction.DoesNotExist:
        return render(request, "auctions/error.html", {
            "code": 404,
            "message": "The auction does not exist."
        })

    user = request.user
    watching = False
    highest_bidder = None
    bid_Num = Bid.objects.filter(auction=auction).count()
    comments = Comment.objects.filter(auction=auction).order_by("-cm_date")
    highest_bid = Bid.objects.filter(auction=auction).aggregate(Max('bid_price'))

    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=user, auctions=auction)
        if watchlist.exists():
            watching = True

    if request.method == "GET":
        form = biddingForm()
        commentForm = commentForm()

        if not auction.closed:
            return render(request, "auctions/listing.html", {
                "auction": auction,
                "form": form,
                "user": user,
                "bid_Num": bid_Num,
                "commentForm": commentForm,
                "comments": comments,
                "watching": watching
            })

        if highest_bid['bid_price__max'] is None:
            messages.info(request, 'The bid is closed, and no bidder.')
        else:
            highest_bid = Bid.objects.filter(auction=auction, bid_price=highest_bid['bid_price__max']).first()
            highest_bidder = highest_bid.bidder
            if user == highest_bidder:
                messages.info(request, 'Congratulations. You won the bid.')
            else:
                messages.info(request, f'The winner of the bid is {highest_bidder.username}')

        return render(request, "auctions/listing.html", {
            "auction": auction,
            "form": form,
            "user": user,
            "highest_bidder": highest_bidder,
            "bid_Num": bid_Num,
            "commentForm": commentForm,
            "comments": comments,
            "watching": watching
        })


@login_required(login_url="login")
def bidding(request, auction_id):
    if request.method == "POST":
        auction = get_object_or_404(Auction, pk=auction_id)

        # Get the highest bid for the auction
        highest_bid = Bid.objects.filter(auction=auction).order_by("-bid_price").first()
        highest_bid_price = auction.current_bid if highest_bid is None else highest_bid.bid_price

        form = biddingForm(request.POST, request.FILES)

        if auction.closed:
            messages.error(request, 'The auction listing is closed.')
            return HttpResponseRedirect(reverse("listing", args=(auction.id,)))
        else:
            if form.is_valid():
                bid_price = form.cleaned_data["bid_price"]

                if bid_price > auction.starting_bid and bid_price > (auction.current_bid or highest_bid_price):
                    new_bid = form.save(commit=False)
                    new_bid.bidder = request.user
                    new_bid.auction = auction
                    new_bid.save()

                    auction.current_bid = bid_price
                    auction.save()

                    messages.success(request, 'Your bid offer is made successfully.')
                else:
                    messages.error(request, 'Please submit a valid bid offer. Your bid must be higher than the starting bid and current price.')

                return HttpResponseRedirect(reverse("listing", args=(auction.id,)))
            else:
                messages.error(request, 'Please submit a valid bid offer. Your bid must be higher than the starting bid and current price.')
                return HttpResponseRedirect(reverse("listing", args=(auction.id,)))


@login_required(login_url="login")
def close(request, auction_id):
    if request.method == "POST":
        auction = get_object_or_404(Auction, pk=auction_id)

        if request.user != auction.seller:
            messages.error(request, 'The request is not allowed.')
        else:
            auction.closed = True
            auction.save()
            messages.success(request, 'The auction listing is closed successfully.')

        return HttpResponseRedirect(reverse("listing", args=(auction.id,)))


@login_required(login_url="login")
def comment(request, auction_id):
    if request.method == "POST":
        auction = get_object_or_404(Auction, pk=auction_id)
        form = commentForm(request.POST, request.FILES)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.auction = auction
            new_comment.save()

            messages.success(request, 'Your comment is received successfully.')

            return HttpResponseRedirect(reverse("listing", args=(auction.id,)))
        else:
            messages.error(request, 'Please submit a valid comment.')


@login_required(login_url="login")
def add(request, auction_id):
    if request.method == "POST":
        auction = get_object_or_404(Auction, pk=auction_id)

        if Watchlist.objects.filter(user=request.user, auctions=auction).exists():
            messages.error(request, 'You already added this listing to your watchlist.')
        else:
            watchlist, created = Watchlist.objects.get_or_create(user=request.user)
            watchlist.auctions.add(auction)
            messages.success(request, 'The listing is added to your Watchlist.')

        return HttpResponseRedirect(reverse("listing", args=(auction.id,)))

 
@login_required(login_url="login")
def remove(request, auction_id):
    if request.method == "POST":
        try:
            auction = Auction.objects.get(pk=auction_id)
        except Auction.DoesNotExist:
            return render(request, "auctions/error.html", {
                "code": 404,
                "message": "The auction does not exist."
            })
        
        watchlist = Watchlist.objects.get_or_create(user=request.user)[0]
        
        if watchlist.auctions.filter(pk=auction_id).exists():
            watchlist.auctions.remove(auction)
            messages.success(request, 'The listing is removed from your watchlist.')
        else:
            messages.error(request, 'You cannot remove a listing that is not in your watchlist.')
        
        return HttpResponseRedirect(reverse("listing", args=(auction.id,)))
