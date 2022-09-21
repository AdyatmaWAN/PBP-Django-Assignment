from django.shortcuts import render
from mywatchlist.models import WatchListItem
from django.core import serializers
from django.http import HttpResponse
# Create your views here.

def show_watchlist(request):
    return HttpResponse("Hello, world. You're at the mywatchlist index.")

def show_mywatchlist_html(request):
    data_watchlist = WatchListItem.objects.all()
    watched = 0
    unwatched = 0
    message = ""
    for film in data_watchlist:
        if film.watched:
            watched += 1
        else:
            unwatched += 1
    print(watched)
    if watched >= unwatched:
        message = "Selamat, kamu sudah banyak menonton!"
    else:
        message = "Wah, kamu masih sedikit menonton!"

    context = {
        "watchlist": data_watchlist,
        "message": message,
    }
    return render(request, 'mywatchlist.html', context)

def show_mywatchlist_json(request):
    data_watchlist = WatchListItem.objects.all()
    return HttpResponse(serializers.serialize("json", data_watchlist), content_type="application/json")

def show_mywatchlist_xml(request):
    data_watchlist = WatchListItem.objects.all()
    return HttpResponse(serializers.serialize("xml", data_watchlist), content_type="application/xml")
