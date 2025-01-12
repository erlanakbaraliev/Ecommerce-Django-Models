from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "Listings": Listing.objects.filter(is_active=True),
        "categories": Category.objects.all()
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

def createListing(request):
    if(request.method == "POST"):
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["image_url"]
        price = float(request.POST["price"])
        
        user = request.user
        is_active = True
        categoryName = request.POST["category"]
        category = Category.objects.get(categoryName=categoryName)
        bid = Bid(bid=price, user=user)
        bid.save()

        newListing = Listing(
            title=title, 
            description=description, 
            image_url=image_url, 
            price=bid, 
            owner=user, 
            is_active=is_active, 
            category=category,
            bidCount=0
        )
        newListing.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/createListing.html", {
            "categories": Category.objects.all()
        })

def displayWithCategory(request):
    if request.method == "POST":
        categoryStr = request.POST["category"]
        category = Category.objects.get(categoryName=categoryStr)
        return render(request, "auctions/index.html", {
            "Listings": Listing.objects.filter(is_active=True, category=category),
            "categories": Category.objects.all()
        })
    
def displayPage(request, listingTitle):
    listing = Listing.objects.get(title=listingTitle)
    isOwner = request.user == listing.owner

    return render(request, "auctions/displayPage.html", {
        "listing": listing,
        "bidCount": listing.bidCount,
        "isUserInWatchlist": request.user in listing.watchlist.all(),
        "isOwner": isOwner
    })

def watchList(request):
    user = request.user
    watchlist = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })

def addToWatchlist(request, listingTitle):
    listing = Listing.objects.get(title=listingTitle)
    listing.watchlist.add(request.user)

    return HttpResponseRedirect(reverse("displayPage", args=(listingTitle,)))

def removeFromWatchlist(request, listingTitle):
    listing = Listing.objects.get(title=listingTitle)
    listing.watchlist.remove(request.user)

    return HttpResponseRedirect(reverse("displayPage", args=(listingTitle,)))

def addComment(request, listingTitle):
    listing = Listing.objects.get(title=listingTitle)
    newComment = Comment(
        author=request.user, 
        listing=listing, 
        message=request.POST['comment']
    )
    newComment.save()

    return HttpResponseRedirect(reverse("displayPage", args=(listingTitle,)))

def addBid(request, listingTitle):
    listing = Listing.objects.get(title=listingTitle)
    bidAmount = request.POST["bidAmount"]
    newBid = Bid(bid=bidAmount, user=request.user)
    newBid.save()

    listing.price = newBid
    listing.save()
    listing.leadingUser = request.user
    listing.save()
    listing.bidCount += 1
    listing.save()

    return HttpResponseRedirect(reverse("displayPage", args=(listingTitle,)))

def closeAuction(request, listingTitle):
    listing = Listing.objects.get(title=listingTitle)
    listing.is_active = False
    listing.save()

    return HttpResponseRedirect(reverse("displayPage", args=(listingTitle,)))