from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import User, AuctionListing, Category, Bid, Comment
from .forms import AuctionForm, BidForm, CommentForm
from django.contrib import messages



# active listings go here?
def index(request):
    if request.method == "POST":
        acution_form = AuctionForm(request.POST, request.FILES)
        if acution_form.is_valid():
            acution_form.save()
            messages.success(request, (f'\"{ acution_form.cleaned_data["title"] }\" was successfully added!'))
            return redirect("auctions:index")
        else:
            messages.error(request, 'Error saving form')
    else: 
        acution_form = AuctionForm()
    auctions = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {'acution_form':acution_form, 'auctions':auctions})


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")


def listing(request, listing_id):
    print(
        f"Debugging: Listing ID is {listing_id}"
    )  # This will print the listing ID to your console

    listing = get_object_or_404(listing, id=listing_id)
    print(
        f"Debugging: Listing object is {listing}"
    )  # This will print the listing object to your console

    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "bids": listing.bids.all(),
            "comments": listing.comments.all(),
        },
    )
    
def bid(request, listing_id): 
    print(f"Debugging: Listing ID is {listing_id}") # This will print the listing ID to your console
    listing = get_object_or_404(listing, id=listing_id)
    print(f"Debugging: Listing object is {listing}") # This will print the listing object to your console
    return render(request, "auctions/bid.html", {
        "listing": listing,
        "bids": listing.bids.all(),
        "comments": listing.comments.all(),
    })


def create_listing(request):
    return render(request, "auctions/create_listing.html")


def watchlist(request):
    return render(request, "auctions/watchlist.html")


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {'categories': categories})
