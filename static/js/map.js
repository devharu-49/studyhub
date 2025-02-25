document.addEventListener("DOMContentLoaded", function () {
  getLocationAndSendToDjango(); // ページが読み込まれたら実行
});

function getSelectedTypes() {
  if (localStorage.getItem("selectedTypes") !== null) {
    const selectedTypes = JSON.parse(localStorage.getItem("selectedTypes"));
    return selectedTypes[0];
  } else {
    return "cafe";
  }
}

function getDistance() {
  if (localStorage.getItem("distance") !== null) {
    const distance = JSON.parse(localStorage.getItem("distance"));
    return distance[0];
  } else {
    return 3000;
  }
}

function getLocationAndSendToDjango() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const userLocation = {
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        };
        const selectedTypes = getSelectedTypes();
        const distance = getDistance();

        // 現在地と選択されたタイプをDjangoに送信
        fetchPlacesFromDjango(userLocation, selectedTypes, distance);
      },
      (error) => {
        console.error("位置情報の取得に失敗しました", error);
        alert("位置情報を取得できませんでした");
      }
    );
  } else {
    alert("このブラウザでは位置情報を取得できません");
  }
}

function fetchPlacesFromDjango(location, placeTypes, distance) {
  const url = `/api/send_location/`;
  const data = {
    latitude: location.latitude,
    longitude: location.longitude,
    types: placeTypes,
    distance: distance,
  };

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"), // CSRFトークンを追加
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      localStorage.setItem("placesData", JSON.stringify(data.results)); // 結果をローカルに保存
    })
    .catch((error) => {
      console.error("場所情報の取得に失敗しました", error);
    });
}
