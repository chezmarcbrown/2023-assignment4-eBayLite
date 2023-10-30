from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from .models import User, category_list, Listing, Watchlist, Comment, Bid


def index(request):
    category = ''
    listings = Listing._meta.model.objects
    
    if 'category' not in request.GET:
        category = None
    else:
        category = request.GET['category']
        
    if request.GET.get('watchlist'):
        user = User.objects.get(id = request.user.id)
        watchlist_items =  Watchlist.objects.get(user=request.user).item.all().values_list('pk')
        listings = listings.filter(id__in=watchlist_items).values()
        if listings:
            return render(request, "auctions/index.html", {
                "listings": listings,
                "header": f"Watchlist"
            })
        else:
            return render(request, "auctions/index.html", {
                "message": "Your watchlist is empty.",
                "header": f"Watchlist"
            })


    if category is not None:
        listings = listings.filter(category__icontains=category).values()

        if listings:
            return render(request, "auctions/index.html", {
                "listings": listings,
                "header": f"Active Listings: {category}"
            })
        else:
            return render(request, "auctions/index.html", {
                "message": "There are no active listings for this category.",
                "header": f"Active Listings: {category}"
            })
    else:
        listings = Listing._meta.model.objects.all()
        return render(request, "auctions/index.html", {
            "listings": listings,
            "header": "Active Listings"
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
            Watchlist.objects.create(user=user).save()
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create(request):
    if request.method == "POST":
        listing = Listing.objects.create(
            title = request.POST['title'],
            category = request.POST['category'],
            description = request.POST['description'],
            current_bid = request.POST['starting_bid'],
            original_bid = request.POST['starting_bid'],
            is_active = True,
            author = request.user
        )
        listing.save()
        return redirect(index)
    else:
        return render(request, "auctions/create.html", {
            "categories": category_list
        })
    
def listing(request, listing_id):
    item = Listing.objects.get(id = listing_id)
    user = User.objects.get(id = request.user.id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    comments = Comment.objects.filter(item = item)
    bids = Bid.objects.filter(item = item)
    winning_bid = Bid.objects.filter(item=item).all().aggregate(Max('bid', default=item.original_bid))['bid__max']
    winner = ""

    if bids.filter(bid=winning_bid):
        winner = bids.filter(bid=winning_bid).first().author


    if created:
        watchlist.save()

    if request.method == "POST":
        if request.POST.get('comment_input'):
            comment = Comment.objects.create(author=request.user, item=item, comment=request.POST.get('comment_input'))
            comment.save()
            return redirect(listing, listing_id)
        if request.POST.get('place_bid'):
            item.current_bid = request.POST.get('place_bid')
            bid = Bid.objects.create(author=request.user, item=item, bid=request.POST.get('place_bid'))
            item.save()
            bid.save()
            return redirect(listing, listing_id)
    
    return render(request, "auctions/listing.html" , {
        "listing": item,
        "min_bid": item.current_bid + 5,
        "is_on_watchlist": watchlist.item.filter(pk=listing_id).exists(),
        "comments": comments,
        "bids": bids,
        "winner": winner
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": category_list
    })

def watchlist_add_or_remove(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)
    watchlist.save()

    # Add item if it doesn't exist in watchlist
    if not watchlist.item.all().filter(pk=listing_id).exists():
        watchlist.item.add(item)
        watchlist.save()
    # Else remove the item if it does exist
    else:
        watchlist.item.remove(item)
        watchlist.save()
        
    return redirect(listing, listing_id)

def remove_listing(request, listing_id):
    Listing.objects.get(id=listing_id).delete()
    return redirect(index)

def remove_comment(request, comment_id):
    listing_id = Comment.objects.get(id=comment_id).item.id
    Comment.objects.get(id=comment_id).delete()
    return redirect(listing, listing_id)

def remove_bid(request, bid_id):
    listing_id = Bid.objects.get(id=bid_id).item.id
    item = Listing.objects.get(id=listing_id)

    Bid.objects.get(id=bid_id).delete()

    # Get next highest bid
    if Bid.objects.filter(item=item).all():
        item.current_bid = Bid.objects.filter(item=item).all().aggregate(Max('bid', default=item.original_bid))['bid__max']
        item.save()
    else:
        item.current_bid = item.original_bid
        item.save()

    return redirect(listing, listing_id)

def close_listing(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    item.is_active = False
    item.save()
    return redirect(listing, listing_id)