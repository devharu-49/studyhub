// マーカーの表示を管理する関数
function displayDetailMarker(marker) {
  // マーカーの位置を再設定
  const position = marker.getPosition();

  // 新しいマーカーを追加
  const detailMarker = new google.maps.Marker({
    position: position,
    map: map, // mapは事前に初期化されているものと仮定
    title: marker.getTitle(),
  });

  // 他のマーカーを消す
  markers.forEach((m) => m.setMap(null));

  // 詳細マーカーのみを表示
  detailMarker.setMap(map);
}

// 詳細ページのURLから取得したplace_idまたは緯度経度に基づいてマーカーを表示
const placeIdFromUrl = new URLSearchParams(window.location.search).get(
  "place_id"
);
const latFromUrl = parseFloat(
  new URLSearchParams(window.location.search).get("lat")
);
const lngFromUrl = parseFloat(
  new URLSearchParams(window.location.search).get("lng")
);

// ここではplace_idや緯度経度から、markers内で一致するものを探し、表示
markers.forEach((marker) => {
  if (
    marker.getPosition().lat() === latFromUrl &&
    marker.getPosition().lng() === lngFromUrl
  ) {
    displayDetailMarker(marker);
  }
});
