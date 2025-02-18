document.addEventListener("DOMContentLoaded", function () {
  getLocationAndSendToDjango(); // ページが読み込まれたら実行
});

function getSelectedTypes() {
  // const selectedTypes = Array.from(
  //   document.querySelectorAll('input[name="placeType"]:checked')
  // )
  //   .map((input) => input.value)
  //   .join(","); // カンマ区切りで送信
  const selectedTypes = ["primary_school"];
  return selectedTypes;
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

        // 現在地と選択されたタイプをDjangoに送信
        fetchPlacesFromDjango(userLocation, selectedTypes);
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

function fetchPlacesFromDjango(location, placeTypes) {
  const url = `/api/send_location/`;
  const data = {
    latitude: location.latitude,
    longitude: location.longitude,
    types: placeTypes,
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
