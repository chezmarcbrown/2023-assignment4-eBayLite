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
from django.forms import model_to_dict
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import User, AuctionListing, Category, Bid, Comment, Watchlist
from .forms import AuctionForm, BidForm, CommentForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


def index(request):
    # show all active listings
    auctions = AuctionListing.objects.filter(active=True)
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


@login_required
def listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    bid_form = BidForm()
    bids = Bid.objects.filter(listing=listing_id).order_by("-amount")
    comment_form = CommentForm()
    comments = get_comments_data(listing_id)
    is_creator = request.user.is_authenticated and request.user == listing.creator

    return render(
        request,
        "auctions/listing.html",
        {
            "listing": listing,
            "bids": bids,
            "bid_form": bid_form,
            "comments": comments,
            "comment_form": comment_form,
            "is_creator": is_creator,
        },
    )


def get_comments_data(listing_id):
    comment_queryset = Comment.objects.filter(listing=listing_id).order_by("-date_created")
    return [model_to_dict(comment) for comment in comment_queryset]


def getComments(request, listing_id):
    response = {
        'comments': get_comments_data(listing_id)
    }
    return JsonResponse(response)


def comment(request, listing_id):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = comment_form.cleaned_data["content"]
            listing = get_object_or_404(AuctionListing, id=listing_id)
            comment = Comment(commenter=request.user, content=content, listing=listing)
            comment.save()
            return JsonResponse({'status':'success'})


def bid(request, listing_id):
    if request.method != "POST":
        return redirect("auctions:listing", listing_id=listing_id)

    bid_form = BidForm(request.POST)
    if not bid_form.is_valid():
        return redirect("auctions:listing", listing_id=listing_id)

    listing = get_object_or_404(AuctionListing, id=listing_id)
    bid_amount = bid_form.cleaned_data["amount"]

    if bid_amount <= listing.starting_bid:
        messages.error(request, "Bid must be greater than starting bid")
        return redirect("auctions:listing", listing_id=listing.id)

    highest_bid = listing.bids.order_by('-amount').first()
    if highest_bid and bid_amount <= highest_bid.amount:
        messages.error(request, "Bid must be greater than current bid")
        return redirect("auctions:listing", listing_id=listing.id)

    accepted_bid = Bid(bidder=request.user, amount=bid_amount, listing=listing)
    accepted_bid.save()
    return redirect("auctions:listing", listing_id=listing.id)


@login_required
def create_listing(request):
    if request.method == "POST":
        auction_form = AuctionForm(request.POST, request.FILES)
        if auction_form.is_valid():
            auction = AuctionListing(
                creator=request.user,
                title=auction_form.cleaned_data["title"],
                description=auction_form.cleaned_data["description"],
                starting_bid=auction_form.cleaned_data["starting_bid"],
                image_url=auction_form.cleaned_data["image_url"],
                category=auction_form.cleaned_data["category"],
            )
            auction.save()
            messages.success(
                request,
                (f'"{auction.title}" was successfully added!'),
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
    
    
@login_required
def watchlist(request, auction_id):
    if request.method == "POST":
        try:
            auction = AuctionListing.objects.get(id=auction_id)
        except AuctionListing.DoesNotExist:
            return JsonResponse({"error": "Auction does not exist"}, status=400)
       
        watchlist_item, created = Watchlist.objects.get_or_create(user=request.user, auction_listing=auction)
        if not created:  
            watchlist_item.delete()
            added = False
        else:
            added = True

        return JsonResponse({"success": "Watchlist updated", "added": added}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def watchlist_view(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {"watchlist_items": watchlist_items})


@login_required
def remove_from_watchlist(request, auction_id):
    if request.method == "POST":
        try:
            auction = AuctionListing.objects.get(id=auction_id)
        except AuctionListing.DoesNotExist:
            return JsonResponse({"error": "Auction does not exist"}, status=400)

        request.user.watchlist.remove(auction)
        return JsonResponse({"success": "Removed from watchlist"}, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)
    

def category_listings(request, category_id):
    category = Category.objects.get(id=category_id)
    listings = AuctionListing.objects.filter(category=category, active=True)
    return render(request, "auctions/category_listings.html", {"category": category, "listings": listings})


def category(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {"categories": categories})


@login_required
def close_listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)

    if request.user != listing.creator:
        return HttpResponseForbidden("You are not authorized to close this listing.")

    if request.method == "POST":
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse("auctions:listing", args=(listing_id,)))
