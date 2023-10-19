from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, category_list, Listing


def index(request):
    category = ''
    if 'category' not in request.GET:
        category = None
    else:
        category = request.GET['category']

    if category is not None:
        listings = Listing._meta.model.objects.filter(category__icontains=category).values()

        if listings:
            return render(request, "auctions/index.html", {
                "listings": listings,
                "category": category
            })
        else:
            return render(request, "auctions/index.html", {
                "message": "There are no active listings for this category",
                "category": category
            })
    else:
        listings = Listing._meta.model.objects.all()
        return render(request, "auctions/index.html", {
            "listings": listings
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
            bid = request.POST['starting_bid'],
            is_active = True,
            user = request.user
        )
        print(request.user)
        print(request.user)
        listing.save()
        return redirect(index)
    else:
        return render(request, "auctions/create.html", {
            "categories": category_list
        })
    
def listing(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    if request.method == "POST":
        user = User.objects.get(id = request.user.id)
        print(request.POST.get('add_to_watchlist', False))
        if request.POST.get('add_to_watchlist', False) and listing_id not in user.watchlist:
            user.watchlist.append(listing_id)
            print('test test')
            print(user.watchlist)
    return render(request, "auctions/listing.html" , {
        "listing": listing,
        "min_bid": listing.bid + 5
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": category_list
    })