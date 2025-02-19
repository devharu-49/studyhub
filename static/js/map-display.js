function initMap(latitude, longitude) {
  var MyLatLng = new google.maps.LatLng(latitude, longitude);
  var Options = {
    zoom: 15,
    center: MyLatLng,
    mapTypeId: "roadmap",
  };
  var map = new google.maps.Map(document.getElementById("map"), Options);
}

function fetchLocationData() {
  fetch("/api/get_location/")
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
