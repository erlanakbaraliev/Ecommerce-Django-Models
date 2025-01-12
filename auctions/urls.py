from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.createListing, name="createListing"),
    path("displayWithCategory", views.displayWithCategory, name="displayWithCategory"),
    path("index/<str:listingTitle>", views.displayPage, name="displayPage"),
    path("watchList", views.watchList, name="goodList"),
    path("index/<str:listingTitle>/addToWatchlist", views.addToWatchlist, name="addToWatchlist"),
    path("index/<str:listingTitle>/removeFromWatchlist", views.removeFromWatchlist, name="removeFromWatchlist"),
    path("index/<str:listingTitle>/addComment", views.addComment, name="addComment"),
    path("index/<str:listingTitle>/addBid", views.addBid, name="addBid"),
    path("index/<str:listingTitle>/closeAuction", views.closeAuction, name="closeAuction"),
]
