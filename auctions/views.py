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
    listings = Listing._meta.model.objects.all()
    watchlist = None
    user = None

    if User.objects.filter(id=request.user.id).exists():
        user = User.objects.get(id = request.user.id)
        watchlist =  Watchlist.objects.get(user=request.user).item.all()
    
    if 'category' not in request.GET:
        category = None
    else:
        category = request.GET['category']
        
    # Display watchlist
    if request.GET.get('watchlist'):
        user = User.objects.get(id = request.user.id)
        watchlist_items =  watchlist.values_list('pk')
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

    # Display listings belonging to category
    if category is not None:
        listings = listings.filter(category__icontains=category).all()

        if listings:
            return render(request, "auctions/index.html", {
                "listings": listings,
                "watchlist": watchlist,
                "header": f"Active Listings: {category}"
            })
        else:
            return render(request, "auctions/index.html", {
                "message": "There are no active listings for this category.",
                "header": f"Active Listings: {category}"
            })
        
    return render(request, "auctions/index.html", {
        "listings": listings,
        "watchlist": watchlist,
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
    
    
def add_comment(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    comment, created = Comment.objects.get_or_create(author=request.user)
    comment.save()

    comment_text = request.POST.get('comment_input')

    if comment_text:
        comment = Comment.objects.create(author=request.user, item=item, comment=comment_text)
        comment.save()

    return HttpResponse(200)    
    

def listing(request, listing_id):
    item = Listing.objects.get(id = listing_id)
    comments = Comment.objects.filter(item = item)
    bids = Bid.objects.filter(item = item)

    winning_bid = Bid.objects.filter(item=item).all().aggregate(Max('bid', default=item.original_bid))['bid__max']
    winner = ""

    if bids.filter(bid=winning_bid):
        winner = bids.filter(bid=winning_bid).first().author
        
    if (request.user.id == None):
        return render(request, "auctions/listing.html" , {
            "listing": item,
            "min_bid": item.current_bid + 5,
            "comments": comments,
            "bids": bids,
            "winner": winner
    })
    
    user = User.objects.get(id = request.user.id)
    watchlist, created = Watchlist.objects.get_or_create(user=request.user)

    if created:
        watchlist.save()
        
    is_in_watchlist = watchlist.item.all().filter(pk=listing_id).exists()
    watchlist = list(watchlist.item.all().values_list())
    
    if request.method == "POST":
        if request.POST.get('comment_input'):
            return add_comment(request)
        if request.POST.get('place_bid'):
            item.current_bid = request.POST.get('place_bid')
            bid = Bid.objects.create(author=request.user, item=item, bid=request.POST.get('place_bid'))
            item.save()
            bid.save()
            return redirect(listing, listing_id)
    
    return render(request, "auctions/listing.html" , {
        "listing": item,
        "min_bid": item.current_bid + 5,
        "is_in_watchlist": is_in_watchlist,
        "watchlist": watchlist,
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
        
    return HttpResponse(200)

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
