document.addEventListener("DOMContentLoaded", function () {
  getLocation(); // ページが読み込まれたら実行
});

function getLocation() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(sendLocation, showError);
  } else {
    alert("Geolocation is not supported by this browser.");
  }
}

function sendLocation(position) {
  const lat = position.coords.latitude;
  const lng = position.coords.longitude;
  console.log("現在地:", lat, lng);

  // Djangoバックエンドへ送信
  fetch("/api/send_location/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"), // DjangoのCSRF対策
    },
    body: JSON.stringify({ latitude: lat, longitude: lng }),
  })
    .then((response) => response.json())
    .then((data) => console.log("サーバーの応答:", data))
    .catch((error) => console.error("エラー:", error));
}

function showError(error) {
  console.error("エラー:", error);
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
