document.addEventListener("DOMContentLoaded", function () {
      const form = document.querySelector("form");
      const btn = document.getElementById("login-btn");
      const spinner = document.getElementById("loading-spinner");
      const loginText = document.querySelector(".login-text")

      form.addEventListener("submit", function () {
            btn.disabled = true;
            btn.classList.add("opacity-75", "cursor-not-allowed");
            spinner.classList.remove("hidden");
            loginText.classList.add("hidden");
      });
})