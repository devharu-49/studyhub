let map;
let markers = [];

function initMap(latitude, longitude) {
  const placesData = JSON.parse(localStorage.getItem("placesData")); // ローカルストレージからデータを取得
  var MyLatLng = new google.maps.LatLng(latitude, longitude);
  var Options = {
    zoom: 15,
    center: MyLatLng,
    mapTypeId: "roadmap",
  };
  map = new google.maps.Map(document.getElementById("map"), Options);

  if (!placesData || placesData.length === 0) {
    // alert("近くの施設が見つかりませんでした。");
    return;
  }

  // マーカーの設定
  placesData.forEach((place) => {
    if (place.geometry && place.geometry.location) {
      const position = {
        lat: place.geometry.location.lat,
        lng: place.geometry.location.lng,
      };
      addMarker(position, place.name, place.place_id);
    }
  });

  localStorage.setItem("markers", JSON.stringify(markers));

  markers.forEach((marker) => {
    marker.setMap(map);
  });
}

function fetchLocationData() {
  fetch("/search/get_location/")
    .then((response) => response.json())
    .then((data) => {
      console.log("Djangoから取得した位置情報:", data);
      const latitude = data.latitude;
      const longitude = data.longitude;

      // Google Maps の初期化
      initMap(latitude, longitude);
    })
    .catch((error) => console.error("エラー:", error));
}

// Google Maps APIのスクリプトが読み込まれた後に実行
document.addEventListener("DOMContentLoaded", function () {
  fetchLocationData();
});

// 📍 マーカーを追加（赤ピン）
function addMarker(location, title, place_id) {
  const marker = new google.maps.Marker({
    position: location,
    map: map,
    title: title,
    icon: {
      url: "http://maps.google.com/mapfiles/ms/icons/red-dot.png", // 🔴 赤ピン
    },
  });

  // マーカーがクリックされたときに詳細ページに遷移する
  marker.addListener("click", function () {
    window.location.href = `/search/detail/?lat=${location.lat}&lng=${location.lng}&place_id=${place_id}`;
  });

  // マーカーを配列に追加
  markers.push(marker);
}

// ❌ 既存のマーカーを削除
function clearMarkers() {
  markers.forEach((marker) => marker.setMap(null));
  markers = [];
}
