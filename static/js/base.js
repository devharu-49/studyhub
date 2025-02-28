document.getElementById("hamburger").addEventListener("click", (event) => {
  const spans = event.currentTarget.querySelectorAll("span");
  const nav = document.getElementById("nav");

  if (spans.length >= 3) {
    spans[0].classList.toggle("rotate-45");
    spans[0].classList.toggle("translate-y-2.5");
    spans[1].classList.toggle("opacity-0");
    spans[2].classList.toggle("-rotate-45");
    spans[2].classList.toggle("-translate-y-2.5");
    nav.classList.toggle("right-0");
    nav.classList.toggle("right-[-100%]");
  }
});

function resetSessionStorage() {
  console.log("logout");
  sessionStorage.clear();
  document.logoutForm.submit();
}
