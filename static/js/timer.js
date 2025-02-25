let currentTimerValue; // 現在のタイマー表示時間
let timerInterval; //
let timeEditer; // タイマー編集要素
let times; //稼働中タイマーの時間管理
let isRunning; // タイマーの稼働状況
let isWorking = true; // ポモドーロのフェーズ
let isPomodoro; //ポモドーロON/OFF
let remainingTime; // タイマー残り時間(ミリ秒)
let isTimerEdited; // タイマー編集履歴

document.addEventListener("DOMContentLoaded", () => {
  console.log("sessionstrage", sessionStorage);
  currentTimerValue = document.getElementById("time");
  timeEditer = document.getElementById("edit-time");
  isWorking =
    document.getElementById("time").getAttribute("data-working") === "True";
  isPomodoro =
    document.getElementById("time").getAttribute("data-pomodoro") === "True";

  // sessionStorage に保存されたデータがあるか確認
  if (sessionStorage.getItem("times")) {
    times = JSON.parse(sessionStorage.getItem("times")); // あれば格納
  } else {
    // localStorageに保存されたデータがなければ作成
    times = {
      startTime: 0, // タイマー開始時刻
      targetTime: 0, // タイマー終了時刻
      passedTime: 0, // 経過時間
    };
  }

  // isRunnigにtrueが保存されているか確認
  if (sessionStorage.getItem("isRunning") === "true") {
    console.log(times);
    if (Object.values(times).every((value) => value === 0)) {
      startTimer();
    } else {
      timerInterval = setInterval(() => updateTimer(times.targetTime), 500); //1秒間隔でタイマー更新関数実行
      isRunning = true;
      toggleButton();
    }
    // requestAnimationFrame(updateTimer(times.targetTime));
  } else {
    // タイマー表示時間が保存されているか確認
    if (sessionStorage.getItem("displayTime")) {
      currentTimerValue.innerHTML = sessionStorage.getItem("displayTime");
    }
  }

  // 編集履歴の有無
  isTimerEdited = sessionStorage.getItem("isTimerEdited") === "true";

  // 時間表示部分がクリックされたとき編集できるようにする
  currentTimerValue.addEventListener("click", () => {
    startEditTime();
  });

  sessionStorage.clear();
});

// 表示時間更新
function updateTimer(targetTime) {
  if (isRunning === false) return;

  const now = new Date().getTime(); // 基準時間からの経過時間
  const remainingTime = targetTime - now; // 残り時間の算出

  if (remainingTime < 0) {
    finishTimer();
    return;
  }
  currentTimerValue.innerHTML = millisecondsToTime(remainingTime); // html更新
}

//タイマー開始
function startTimer() {
  if (isRunning) return;
  console.log("start!!");

  if (isTimerEdited && times.passedTime == 0 && isWorking) {
    console.log("update!!");
    updateSetTime();
  }

  toggleButton(); // ボタン切り替え
  isRunning = true; // 稼働中に変更
  times.startTime = new Date().getTime(); // 開始時間を格納
  times.targetTime =
    times.startTime + timeToMilliseconds(currentTimerValue.innerHTML); //終了時刻を格納

  timerInterval = setInterval(() => updateTimer(times.targetTime), 500); //1秒間隔でタイマー更新関数実行
  // requestAnimationFrame(updateTimer(times.targetTime));
}

//タイマー停止
function stopTimer() {
  if (isRunning !== true) return; //稼働していないなら何もしない

  isRunning = false; // 停止中に変更
  times.passedTime += new Date().getTime() - times.startTime; // 経過時間を追加
  clearInterval(timerInterval); // 定期実行停止
  toggleButton(); // ボタン変更
}

//タイマー終了
function finishTimer() {
  stopTimer();
  if (isWorking) {
    document.getElementById("registered-time").value = millisecondsToTime(
      times.passedTime
    );
    toggleTimerModal();
  } else {
    toggleBreakTimeModal();
  }
}

// タイマー編集開始
function startEditTime() {
  if (isRunning) {
    return; // タイマー稼働中は無効
  }
  timeEditer = document.getElementById("edit-time");
  if (timeEditer.classList.contains("flex")) return;

  console.log(currentTimerValue.innerHTML);
  const timeParts = currentTimerValue.innerHTML.split(":");
  console.log("ここからここから");
  console.log(timeParts);
  const inputs = timeEditer.querySelectorAll(".input-time"); // 出力はNodeList
  console.log(inputs);
  [...inputs].map((input, index) => {
    input.value = timeParts[index];
    // 編集箇所以外がクリックされたとき非表示にする
    document.addEventListener("click", clickOutsideTimer);
  });
  toggleTimeEditer();
}

// タイマー編集終了
function endEditTime() {
  if (isRunning) return; // タイマー稼働中は無効
  const inputs = timeEditer.querySelectorAll(".input-time"); // 出力はNodeList 配列じゃない
  const inputTimes = [...inputs].map((input) => input.value); // 配列に直してmap関数を使う
  if (inputTimes.some((value) => !/^\d+$/.test(value))) {
    if (
      document.getElementById("time-edit-error").classList.contains("hidden")
    ) {
      document.getElementById("time-edit-error").classList.remove("hidden");
    }
    return; // 半角数字以外が含まれていたら何もしない
  }
  currentTimerValue.innerHTML = `${inputTimes[0].padStart(2, "0")}:${inputTimes[1].padStart(2, "0")}:${inputTimes[2].padStart(2, "0")}`;
  if (
    !document.getElementById("time-edit-error").classList.contains("hidden")
  ) {
    document.getElementById("time-edit-error").classList.add("hidden");
  }
  toggleTimeEditer();
  isTimerEdited = true;
  document.removeEventListener("click", clickOutsideTimer); // イベントリスナーの削除
}

// タイマー編集終了イベントを起こす関数
function clickOutsideTimer(event) {
  if (timeEditer.contains(event.target) || event.target === currentTimerValue)
    return;
  endEditTime();
}

// Enterキーが押されたときタイマー編集を終了
document.getElementById("edit-time").addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    endEditTime();
  }
});

// ボタン変更
function toggleButton() {
  const startButtonClass = document.getElementById("timer-start-btn").classList;
  const stopButtonClass = document.getElementById("timer-stop-btn").classList;

  startButtonClass.toggle("flex");
  startButtonClass.toggle("hidden");

  stopButtonClass.toggle("flex");
  stopButtonClass.toggle("hidden");
}

// タイマー終了モーダル表示
function toggleTimerModal() {
  document.getElementById("timer-modal").classList.toggle("flex");
  document.getElementById("timer-modal").classList.toggle("hidden");
}

// 休憩終了モーダル表示
function toggleBreakTimeModal() {
  document.getElementById("breaktime-modal").classList.toggle("flex");
  document.getElementById("breaktime-modal").classList.toggle("hidden");
}

// タイマー編集切り替え
function toggleTimeEditer() {
  if (isRunning) return; // タイマー稼働中は無効
  currentTimerValue.classList.toggle("block");
  currentTimerValue.classList.toggle("hidden");
  timeEditer.classList.toggle("flex");
  timeEditer.classList.toggle("hidden");
  document
    .getElementById("timer-start-btn")
    .classList.toggle("pointer-events-none");
  document
    .getElementById("timer-finish-btn")
    .classList.toggle("pointer-events-none");
}

// ミリ秒から表示時間に変換
function millisecondsToTime(ms) {
  const hours = Math.floor(ms / 1000 / 60 / 60) % 24; //時に直す
  const min = Math.floor(ms / 1000 / 60) % 60; //分に直す
  const sec = Math.round(ms / 1000) % 60; //秒に直す
  //文字列にして表示形式に直す
  const displaytime = `${String(hours).padStart(2, "0")}:${String(min).padStart(2, "0")}:${String(sec).padStart(2, "0")}`;

  return displaytime;
}

// 表示時間からミリ秒に変換
function timeToMilliseconds(timeString) {
  const timeParts = timeString.split(":");
  const Millisec =
    (Number(timeParts[0]) * 3600 +
      Number(timeParts[1]) * 60 +
      Number(timeParts[2])) *
    1000;

  return Millisec;
}

// 勉強時間登録
function saveTime() {
  console.log(times);
  if (times.passedTime == 0) {
    toggleTimerModal();
    return;
  }

  resetTime();
  if (isPomodoro) {
    isRunning = true;
    console.log("isRunning", isRunning);
  }
  document.saveTimeForm.submit();
  console.log("save!!");
}

// timesリセット
function resetTime() {
  times = {
    startTime: 0, // タイマー開始時刻
    targetTime: 0, // タイマー終了時刻
    passedTime: 0, // 経過時間
  };
  toggleTimerModal();
}

// マイページ更新前処理
function updateMyPage() {
  const pomodoroMode = document.querySelector(
    'input[name="is_pomodoro"]:checked'
  )?.value;
  if (!isWorking && !(pomodoroMode === "True")) {
    resetTime();
    isRunning = false;
    isTimerEdited = false;
  }
  document.updateMyPageForm.submit();
}

// sessionstrageへの保存
function saveSessionlStrage() {
  sessionStorage.setItem("times", JSON.stringify(times));
  sessionStorage.setItem("isRunning", isRunning);
  console.log("saveSessionlStrage", isRunning);
  if (
    (!isRunning && times.passedTime !== 0) ||
    (isTimerEdited && times.passedTime == 0)
  ) {
    sessionStorage.setItem("displayTime", currentTimerValue.innerHTML);
    sessionStorage.setItem("isTimerEdited", isTimerEdited);
  }
}

// ページ遷移時sessionstrageに保存
window.addEventListener("unload", () => {
  saveSessionlStrage();
});

// 更新時sessionstrageに保存
window.addEventListener("popstate", () => {
  saveSessionlStrage();
});

// sessionstrageクリア
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    sessionStorage.clear();
  }
});

// csrf対策
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// worktime更新
function updateSetTime() {
  const url = document
    .getElementById("timer-controls")
    .getAttribute("data-url");
  const body = JSON.stringify({ settingtime: currentTimerValue.innerHTML });
  const csrftoken = getCookie("csrftoken");

  fetch(url, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: body,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
    })
    .catch((error) => console.log(error));

  isTimerEdited = false;
}
