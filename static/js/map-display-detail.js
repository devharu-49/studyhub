let lngFromUrl;
let latFromUrl;
let placeIdFromUrl;
// let userLocation;

document.addEventListener("DOMContentLoaded", () => {
  // 詳細ページのURLから取得したplace_idまたは緯度経度に基づいてマーカーを表示
  placeIdFromUrl = new URLSearchParams(window.location.search).get("place_id");
  latFromUrl = parseFloat(
    new URLSearchParams(window.location.search).get("lat")
  );
  lngFromUrl = parseFloat(
    new URLSearchParams(window.location.search).get("lng")
  );

  // getLocation((userLocation) => {
  //   console.log("userLocation", userLocation);
  initMap(
    // userLocation.latitude,
    // userLocation.longitude,
    latFromUrl,
    lngFromUrl
  );
});
// });

// 現在地取得
// function getLocation(callback) {
//   console.log("getLocation");

//   if (navigator.geolocation) {
//     navigator.geolocation.getCurrentPosition((position) => {
//       userLocation = {
//         latitude: position.coords.latitude,
//         longitude: position.coords.longitude,
//       };
//       callback(userLocation); // 取得後にコールバック関数を実行
//     });
//   } else {
//     alert("このブラウザでは位置情報を取得できません");
//   }
// }

// map描画
function initMap(latitude, longitude) {
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
      url: "http://maps.google.com/mapfiles/ms/icons/red-dot.png", // 🔴 赤ピン
    },
  });
  marker.setMap(map);
}
