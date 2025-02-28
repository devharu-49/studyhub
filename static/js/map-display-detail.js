let lngFromUrl;
let latFromUrl;
let placeIdFromUrl;

document.addEventListener("DOMContentLoaded", () => {
  // 詳細ページのURLから取得したplace_idまたは緯度経度取得
  placeIdFromUrl = new URLSearchParams(window.location.search).get("place_id");
  latFromUrl = parseFloat(
    new URLSearchParams(window.location.search).get("lat")
  );
  lngFromUrl = parseFloat(
    new URLSearchParams(window.location.search).get("lng")
  );

  initMap(latFromUrl, lngFromUrl);
});

// map描画
window.initMap(latitude, longitude) {
  var LatLng = new google.maps.LatLng(latitude, longitude);
  var Options = {
    zoom: 15,
    center: LatLng,
    mapTypeId: "roadmap",
  };
  map = new google.maps.Map(document.getElementById("map"), Options);

  // 📍 マーカーを追加（赤ピン）
  const marker = new google.maps.Marker({
    position: { lat: latitude, lng: longitude },
    map: map,
    // title: title,
    icon: {
      url: "https://maps.googleapis.com/mapfiles/ms/icons/red-dot.png", // 🔴 赤ピン
    },
  });
  marker.setMap(map);
}
