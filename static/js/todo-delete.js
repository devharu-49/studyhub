// モーダル要素を取得
const delitemodal = document.getElementById("todo-delete-modal");

// ゴミ箱アイコンが押されたときにモーダルを表示
function showModal(event) {
  const todoName = document.getElementById("delete-todo-title");
  const taskId = event.target.closest("button").getAttribute("data-task-id"); // task.idを取得
  todoName.innerHTML = event.target.closest("li").querySelector(".todo-name").innerText;  // タスク名を設定
  delitemodal.style.display = "flex";  // モーダルを表示


  // モーダルの削除フォームに taskId を設定
  const deleteForm = document.getElementById("delete-form");
  deleteForm.action = `/todo/delete/${taskId}/`;  // タスクのIDを削除URLに追加
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

