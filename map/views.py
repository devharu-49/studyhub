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
    places_result = gmaps.places_nearby(location=location, radius=distance, language="ja", type=place_type)
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
  query = request.GET.get('query', '')  # 検索ワード
  place = request.GET.get('place', 'cafe')  # 選ばれた場所
  distance = request.GET.get('distance', 3000)  # 距離（デフォルトで3000）
  global latest_location

  lat = latest_location.get('latitude')
  lon = latest_location.get('longitude')

  location = (float(lat), float(lon)) # まとめる
  places_result = gmaps.places_nearby(location=location, radius=distance, language="ja", type=place)

  distances = []  # 距離を格納するリスト

  # 各検索結果に対して徒歩の距離を計算
  for place in places_result["results"]:
      place_lat = place["geometry"]["location"]["lat"]
      place_lon = place["geometry"]["location"]["lng"]

      # 現在地と検索場所の間の徒歩距離を計算
      origin = (lat, lon)
      destination = (place_lat, place_lon)

      # Google Distance Matrix APIを使って徒歩の距離を計算
      distance_matrix_result = gmaps.distance_matrix(origins=[origin], destinations=[destination], mode="walking", language="ja")

      # 徒歩距離を取得
      if distance_matrix_result["status"] == "OK":
          distance_text = distance_matrix_result["rows"][0]["elements"][0]["distance"]["text"]
          place["walking_distance"] = distance_text  # 徒歩距離をplaceの情報に追加

      distances.append(place)
  return render(request, "search_result.html", {"results" : places_result["results"], "distances" : distances})