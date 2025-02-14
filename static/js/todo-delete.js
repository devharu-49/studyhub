// モーダル要素を取得
const delitemodal = document.getElementById("todo-delete-modal");

// ゴミ箱アイコンが押されたときにモーダルを表示
function showModal(event, taskId, taskTitle) {
  const todoName = document.getElementById("dekete-todo-title");
  todoName.innerHTML = taskTitle;
  delitemodal.style.display = "flex";
  
  // 削除フォームのactionを設定（taskIdを送信する）
  const deleteForm = document.getElementById("delete-form");
  deleteForm.action = `/todo/delete/${taskId}/`;  // 適切なURLに変更
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
