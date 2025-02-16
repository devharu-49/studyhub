from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import googlemaps
import json

API_KEY = "AIzaSyAuDf-txlL1EEte-Iqolx0CvtvxazFkF6k"
gmaps = googlemaps.Client(key=API_KEY)

latest_location = {}

# Create your views here.
@csrf_exempt  # CSRF対策を無効化（適宜、別の方法で対策推奨）
def receive_location(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')

            print(f"受け取った位置情報: 緯度={latitude}, 経度={longitude}")

            latest_location = {'latitude': latitude, 'longitude': longitude}

            return JsonResponse({"message": "位置情報を受け取りました"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid request"}, status=400)


def get_location(request):
  global latest_location
  if not latest_location:
     latest_location = {'latitude': 35.6811673, 'longitude': 139.7670516}
  return JsonResponse(latest_location)


def search(request):
  global latest_location

  if not latest_location:
    lat = 35.6811673
    lon = 139.7670516
  else:
    lat = latest_location.get('latitude')
    lon = latest_location.get('longitude')

  # distance = request.GET["distance"] #半径
  distance = 2000


  location = (float(lat), float(lon)) # まとめる
  places_result = gmaps.places_nearby(location=location, radius=distance, type="cafe")
  return render(request, "search.html", {"results" : places_result["results"]})

def search_detail(request):
  global latest_location

  if not latest_location:
    lat = 35.6811673
    lon = 139.7670516
  else:
    lat = latest_location.get('latitude')
    lon = latest_location.get('longitude')

  # distance = request.GET["distance"] #半径
  distance = 2000


  location = (float(lat), float(lon)) # まとめる
  places_result = gmaps.places_nearby(location=location, radius=distance, type="cafe")
  return render(request, "search_detail.html", {"results" : places_result["results"]})

def search_result(request):
  global latest_location

  if not latest_location:
    lat = 35.6811673
    lon = 139.7670516
  else:
    lat = latest_location.get('latitude')
    lon = latest_location.get('longitude')

  # distance = request.GET["distance"] #半径
  distance = 2000


  location = (float(lat), float(lon)) # まとめる
  places_result = gmaps.places_nearby(location=location, radius=distance, type="cafe")
  return render(request, "search_result.html", {"results" : places_result["results"]})