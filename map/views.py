from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import googlemaps
import json

API_KEY = "AIzaSyAuDf-txlL1EEte-Iqolx0CvtvxazFkF6k"
gmaps = googlemaps.Client(key=API_KEY)

latest_location = {'latitude': 35.6811673, 'longitude': 139.7670516}
places_result = None

# Create your views here.
@csrf_exempt  # CSRF対策を無効化（適宜、別の方法で対策推奨）
def receive_location(request):
  global latest_location
  global places_result
  if request.method == "POST":
    data = json.loads(request.body)
    lat = data.get('latitude')
    lon = data.get('longitude')
    place_type = data.get('types')

    latest_location = {"latitude":lat, "longitude":lon}
    location = (float(lat), float(lon))

    distance = 3000  # 半径3km
    # デフォルトでカフェを検索
    places_result = gmaps.places_nearby(location=location, radius=distance, type=place_type)
    return JsonResponse({"results": places_result["results"]})

def get_location(request):
  global latest_location
  return JsonResponse(latest_location)


def search(request):
  return render(request, "search.html")

def search_detail(request):
  return render(request, "search_detail.html")

def search_result(request):
  global places_result
  if places_result:
    return render(request, "search_result.html", {"results" : places_result["results"]})
  else:
    global latest_location

    lat = latest_location.get('latitude')
    lon = latest_location.get('longitude')

    # distance = request.GET["distance"] #半径
    distance = 3000


    location = (float(lat), float(lon)) # まとめる
    places_result = gmaps.places_nearby(location=location, radius=distance, type="cafe")
    return render(request, "search_result.html", {"results" : places_result["results"]})