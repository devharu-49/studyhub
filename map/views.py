from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import googlemaps
import json
import os
from dotenv import load_dotenv

load_dotenv('.env')

API_KEY = os.getenv("API_KEY")
gmaps = googlemaps.Client(key=API_KEY)

latest_location = {'latitude': 35.6811673, 'longitude': 139.7670516}
places_result = None

@csrf_exempt  # CSRF対策を無効化（適宜、別の方法で対策推奨）
# JSから現在の位置情報を受け取る
def receive_location(request):
  if request.method == "POST":
    data = json.loads(request.body)
    lat = data.get('latitude')
    lon = data.get('longitude')
    place_type = data.get('types')
    distance = data.get('distance')

    request.session["latest_location"] = {"latitude":lat, "longitude":lon}
    location = (float(lat), float(lon))

    # デフォルトでカフェを検索
    places_result = gmaps.places_nearby(location=location, radius=distance, language="ja", type=place_type)
    request.session["places_result"] = places_result
    return JsonResponse({"results": places_result["results"]})

# JSに位置情報を返す
def get_location(request):
  latest_location = request.session["latest_location"]
  return JsonResponse(latest_location)

# 検索ページを返す
def search(request):
  return render(request, "search.html")

# 場所詳細ページを表示
def search_detail(request):
  place_id = (request.GET.get("place_id"))
  lat = float(request.GET.get("lat"))
  lng = float(request.GET.get("lng"))

  if not lat or not lng:
      return render(request, "error.html", {"message": "位置情報が不足しています。"})

  detailed_info = gmaps.place(place_id=place_id, language="ja")  # 施設詳細情報を取得

  latest_location = request.session["latest_location"]

  origin_lat = latest_location['latitude']
  origin_lng = latest_location['longitude']


  # 現在地と検索場所の間の徒歩距離を計算
  origin = (origin_lat, origin_lng)
  destination = (lat, lng)

  # Google Distance Matrix APIを使って徒歩の距離を計算
  distance_matrix_result = gmaps.distance_matrix(origins=[origin], destinations=[destination], mode="walking", language="ja")

  # 徒歩距離を取得
  if distance_matrix_result["status"] == "OK":
      distance_text = distance_matrix_result["rows"][0]["elements"][0]["distance"]["text"]
      distance = distance_text  # 徒歩距離をplaceの情報に追加
  return render(request, "search_detail.html", {"details": detailed_info["result"], "distance": distance})

# 検索結果ページを表示
def search_result(request):
  places_result = request.session["places_result"]
  keyword = request.GET.get('keyword', '')  # 検索ワード
  place = request.GET.get('place', 'cafe')  # 選ばれた場所
  distance = request.GET.get('distance', 3000)  # 距離（デフォルトで3000）
  
  latest_location = request.session["latest_location"]

  lat = latest_location['latitude']
  lon = latest_location['longitude']

  location = (float(lat), float(lon)) # まとめる
  places_result = gmaps.places_nearby(location=location, radius=distance, language="ja", type=place, keyword=keyword)
  results = add_walking_distance_to_results(places_result["results"],lat,lon)

  return render(request, "search_result.html", {"results" : results})

# メインページに表示する項目を取得
def search_near_place(request):
  if not "latest_location" in request.session:
     request.session["latest_location"] = {'latitude': 35.6811673, 'longitude': 139.7670516}

  keyword ='勉強場所'  # 検索ワード
  place = 'cafe'  # 選ばれた場所
  distance = 2000  # 距離
  latest_location = request.session["latest_location"]

  lat = latest_location['latitude']
  lon = latest_location['longitude']

  location = (float(lat), float(lon)) # まとめる
  places_result = gmaps.places_nearby(location=location, radius=distance, language="ja", type=place, keyword=keyword)


  results = add_walking_distance_to_results(places_result["results"],lat,lon)
  sorted_data = sorted(results, key=lambda x: float(x['walking_distance'].split()[0])) # walking_distanceで降順に
  near_place = sorted_data[:3]
      
  return near_place

# 各検索結果に対して徒歩の距離を計算
def add_walking_distance_to_results(results,lat,lon):
  # 検索場所の座標のリストを作成
  place_latlons = []
  for place in results:
      place_lat = place["geometry"]["location"]["lat"]
      place_lon = place["geometry"]["location"]["lng"]

      destination = f"{place_lat}, {place_lon}"
      place_latlons.append(destination)

  # 現在地と検索場所の間の徒歩距離を計算
  origin = f"{lat}, {lon}"
  destinations_str = "|".join(place_latlons)

  # Google Distance Matrix APIを使って徒歩の距離を計算
  distance_matrix_result = gmaps.distance_matrix(origins=origin, destinations=destinations_str, mode="walking", language="ja")

  # 徒歩距離を取得
  for i, element in enumerate(distance_matrix_result["rows"][0]["elements"]):
    if element["status"] == "OK" and i < len(results):
        results[i]["walking_distance"] = element["distance"]["text"]

  return results