
const form = document.querySelector("form");
const btn = document.getElementById("change-password-btn");
const spinner = document.getElementById("loading-spinner");

form.addEventListener("submit", function (e) {
      e.preventDefault()

      btn.disabled = true;
      btn.classList.add("opacity-75", "cursor-not-allowed");
      spinner.classList.remove("hidden");
});
