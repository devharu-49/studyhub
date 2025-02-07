// モーダル要素を取得
const delitemodal = document.getElementById("todo-delite-modal");

// ゴミ箱アイコンが押されたときにモーダルを表示
function showModal(event) {
  const todo = event.target.closest("li").querySelector(".todo-name");
  const todoname = todo.innerHTML;
  delitemodal.querySelector(".delite-todo-name").innerHTML = todoname;
  delitemodal.style.display = "flex";
}

// キャンセルが押されたときにモーダルを非表示
function hiddenModal(event) {
  delitemodal.style.display = "none";
}

// モーダル以外がクリックされたとき非表示にする
delitemodal.addEventListener("click", function (event) {
  if (event.target !== delitemodal.querySelector(".modal-overlay")) return;
  delitemodal.style.display = "none";
});
