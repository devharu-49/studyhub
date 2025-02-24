// Chart.js をインポート
// import Chart from "chart.js/auto";
console.log(durationData);
// キャンバスを取得
const canvas = document.getElementById("myChart");

// チャートのコンテキストを取得
const ctx = canvas.getContext("2d");

// チャートのデータ
const data = {
  labels: durationData["dates"],
  datasets: [
    {
      // label: "勉強時間",
      data: durationData["times"],
      backgroundColor: "#9fc7aa",
      borderColor: "#9fc7aa",
      borderWidth: 1,
    },
  ],
};

// チャートのオプション
const options = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      title: {
        display: true,
        text: "作業時間(分)",
      },
    },
  },
  plugins: {
    legend: {
      display: false, // レジェンド（ラベル）を非表示にする
    },
  },
};

// 折れ線グラフを作成
const myChart = new Chart(ctx, {
  type: "bar",
  data: data,
  options: options,
});
