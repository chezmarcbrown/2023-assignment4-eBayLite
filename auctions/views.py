# -------------------------------------------------------------------------------------------------------
# This code was developed with assistance from the following:
# - Django https://docs.djangoproject.com/en/4.0/topics/auth/default/#the-login-required-decorator
# - Assited by OpenAI's ChatGPT for additional guidance and debugging
# - https://stackoverflow.com/questions/53594745/what-is-the-use-of-cleaned-data-in-django
# - https://ordinarycoders.com/blog/article/django-modelforms
# - https://docs.djangoproject.com/en/4.2/topics/auth/default/
# - https://www.w3schools.com/django/django_add_bootstrap5.php
# -------------------------------------------------------------------------------------------------------


from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import User, AuctionListing, Category, Bid, Comment
from .forms import AuctionForm, BidForm, CommentForm
from django.contrib import messages


def index(request):
    # show all active listings
    auctions = AuctionListing.objects.all()
    return render(request, "auctions/index.html", {"auctions": auctions})


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
    listing = get_object_or_404(AuctionListing, id=listing_id)
    bid_form = BidForm()
    bids = Bid.objects.all()
    comment_form = CommentForm()
    comments = Comment.objects.all()
    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "bids": bids,
            "bid_form": bid_form,
            "comments": comments,
            "comment_form": comment_form,
        },
    )


def comment(request, listing_id):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = comment_form.cleaned_data["content"]
            listing = get_object_or_404(AuctionListing, id=listing_id)
            comment = Comment(content=content, listing=listing)
            comment.save()
            return redirect("auctions:listing", listing_id=listing.id)


def bid(request, listing_id):
    if request.method == "POST":
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            amount = bid_form.cleaned_data["amount"]
            listing = get_object_or_404(AuctionListing, id=listing_id)
            if amount > listing.starting_bid:
                bid = Bid(amount=amount, listing=listing)
                bid.save()
                return redirect("auctions:listing", listing_id=listing.id)
            else:
                messages.error(request, "Bid must be greater than current bid")
                return redirect("auctions:listing", listing_id=listing.id)


def create_listing(request):
    if not request.user.is_authenticated:
        return redirect("auctions:login")
    if request.method == "POST":
        auction_form = AuctionForm(request.POST, request.FILES)
        if auction_form.is_valid():
            auction_form.save()
            messages.success(
                request,
                (f'"{ auction_form.cleaned_data["title"] }" was successfully added!'),
            )
            return redirect("auctions:index")
        else:
            messages.error(request, "Error saving form")
    else:
        auction_form = AuctionForm()

    auctions = AuctionListing.objects.all()
    return render(
        request,
        "auctions/create_listing.html",
        {"auction_form": auction_form, "auctions": auctions},
    )


def watchlist(request, auction_id):
    if not request.user.is_authenticated:
        return redirect("auctions:login")
    try:
        auction = AuctionListing.objects.get(id=auction_id)
    except AuctionListing.DoesNotExist:
        raise Http404("Auction does not exist")
    # adds to users watchlist
    request.user.watchlist.add(auction)
    watchlist_items = request.user.watchlist.all()
    return render(
        request, "auctions/watchlist.html", {"watchlist_items": watchlist_items}
    )


def watchlist_view(request):
    # shows all items on users watchlist if logged in
    if request.user.is_authenticated:
        watchlist_items = request.user.watchlist.all()
        return render(
            request, "auctions/watchlist.html", {"watchlist_items": watchlist_items}
        )
    else:
        return redirect("auctions:login")


def remove_from_watchlist(request, auction_id):
    auction = AuctionListing.objects.get(id=auction_id)
    # removes from users watchlist
    request.user.watchlist.remove(auction)
    watchlist_items = request.user.watchlist.all()
    return render(
        request, "auctions/watchlist.html", {"watchlist_items": watchlist_items}
    )


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})
