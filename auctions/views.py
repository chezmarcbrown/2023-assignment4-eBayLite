from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import User, AuctionListing, Bid, Comment, Category
from .forms import AuctionListingForm, CommentForm
from django.http import JsonResponse
def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all().order_by('-created_at'),
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


# ======================================================================================================================
@login_required(login_url='login')
def create(request):
    return render(request, "auctions/create.html", {
        'form': AuctionListingForm()
    })


@login_required(login_url='login')
def insert(request):
    if request.method == 'POST':
        form = AuctionListingForm(request.POST, request.FILES)
        if form.is_valid():
            auction = form.save(commit=False)
            auction.user = request.user
            auction.save()

            starting_bid = auction.starting_bid
            bid = Bid(amount=starting_bid, user=request.user, auction=auction)
            bid.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'auctions/create.html', {
                'form': form,
                'error': form.errors
            })
    else:
        form = AuctionListingForm()
        return render(request, 'auctions/create.html', {
            'form': form,
            'error': form.errors
        })


def listing(request, id):
    current = AuctionListing.objects.get(pk=id)
    bid = get_object_or_404(Bid, auction=current)
    comments = Comment.objects.filter(auction=current)
    print("here:", current.image_url.url)
    return render(request, 'auctions/listing.html', {
        'auction': current,
        'user': request.user,
        'bid': bid,
        'comments': comments,
        'comment_form': CommentForm()
    })


@login_required(login_url='login')
def update_bid(request, id):
    amount = request.POST['bid']
    if amount:
        amount = float(amount)
        auction = get_object_or_404(AuctionListing, id=id)
        if amount > get_object_or_404(Bid, id=id).amount:
            bid = get_object_or_404(Bid, id=id)
            bid.user, bid.amount = request.user, amount
            bid.save()
            auction.bid_counter += 1
            auction.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            raise ValidationError('Bid must be greater than current Bid value')
    else:
        raise ValidationError('Bid must be greater than current Bid value')


@login_required(login_url='login')
def close_bid(request, id):
    auction = get_object_or_404(AuctionListing, id=id)
    auction.active, auction.winner = False, request.user.username
    auction.save()
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='login')
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })


@login_required(login_url='login')
def watch(request, id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        auction = get_object_or_404(AuctionListing, id=id)
        request.user.watchlist.add(auction)
        #request.user.watchlist_counter += 1
        #request.user.save()
        return JsonResponse({"success": True, "watchlist_count": request.user.watchlist.count()})
    #return HttpResponseRedirect(reverse('index'))


@login_required(login_url='login')
def unwatch(request, id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        auction = get_object_or_404(AuctionListing, id=id)
        request.user.watchlist.remove(auction)
        #request.user.watchlist_counter -= 1
        #request.user.save()
        return JsonResponse({"success": True, "watchlist_count": request.user.watchlist.count()})
    
    #return HttpResponseRedirect(reverse('wishlist'))


def categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {'categories': categories})

def filter(request):
    # Get the 'category' from the query parameters (it seems to be an ID in the URL).
    category_id = request.GET.get('category')
    listings = []
    categories = Category.objects.all()
    selected_category = None

    # If a category was selected, filter the listings by that category.
    if category_id:
        # Try to find the category by ID since the error indicates 'category=1' which looks like an ID.
        selected_category = get_object_or_404(Category, pk=category_id)
        listings = AuctionListing.objects.filter(category=selected_category)
    else:
        # If no specific category is selected, we might want to show all listings or handle it differently.
        listings = AuctionListing.objects.all()

    context = {
        'categories': categories,
        'selected_category': selected_category,  # This will be None if no category is selected.
        'listings': listings,
    }
    
    return render(request, 'auctions/category.html', context)

@login_required(login_url='login')
def add_comment(request, id):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data['text']
            comment = Comment(
                user=request.user,
                text=comment_text,
                auction=get_object_or_404(AuctionListing, id=id)
            )
            comment.save()

            # Prepare and send the JSON response
            comment_data = {
                'user': str(comment.user),
                'text': comment.text,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
            return JsonResponse(comment_data)
        else:
            return JsonResponse({'error': form.errors}, status=400)
    
