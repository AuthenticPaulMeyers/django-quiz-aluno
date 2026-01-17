
// Disable buttons when they are clicked to avoid double clicking and overloading the server
const form = document.querySelector("form");
const btn = document.getElementById("home-btn");
const spinner = document.getElementById("loading-spinner");

form.addEventListener("submit", function () {
      btn.disabled = true;
      btn.classList.add("opacity-75", "cursor-not-allowed");
      spinner.classList.remove("hidden");
});

