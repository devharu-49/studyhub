let todomodal;
let deletemodal;
let statusmodal;

// モーダル要素を取得
document.addEventListener("DOMContentLoaded", () => {
  todomodal = document.getElementById("todo-modal");
  deletemodal = document.getElementById("delete-modal");
  statusmodal = document.getElementById("statusedit-modal");

  // モーダル以外がクリックされたとき非表示にする
  todomodal.addEventListener("click", function (event) {
    console.log(todomodal);
    if (event.target !== todomodal.querySelector(".modal-overlay")) return;
    hiddenModal();
  });
});

// ゴミ箱アイコンが押されたときにモーダルを表示
function showDeleteModal(event) {
  const todoName = document.getElementById("delete-todo-title");
  const taskId = event.target.closest("button").getAttribute("data-task-id"); // task.idを取得
  todoName.innerHTML = event.target
    .closest("li")
    .querySelector(".todo-name").innerText; // タスク名を設定
  todomodal.style.display = "flex"; // モーダルエリアを表示
  deletemodal.style.display = "flex"; // モーダルを表示

  // モーダルの削除フォームに taskId を設定
  const deleteForm = document.getElementById("delete-form");
  deleteForm.action = `/todo/delete/${taskId}/`; // タスクのIDを削除URLに追加
}

// 完了/未完了アイコンが押されたときにモーダルを表示
function showChangeModal(event) {
  const todoName = document.getElementById("statusedit-todo-title");
  const taskId = event.target.closest("button").getAttribute("data-task-id"); // task.idを取得
  todoName.innerHTML = event.target
    .closest("li")
    .querySelector(".todo-name").innerText; // タスク名を設定
  todomodal.style.display = "flex"; // モーダルエリアを表示
  statusmodal.style.display = "flex"; // モーダルを表示

  // モーダルの削除フォームに taskId を設定
  const changeForm = document.getElementById("statusedit-form");
  changeForm.action = `/todo/status/${taskId}/`; // タスクのIDをURLに追加
}

// キャンセルが押されたときにモーダルを非表示
function hiddenModal() {
  todomodal.style.display = "none";
  statusmodal.style.display = "none";
  deletemodal.style.display = "none";
}
