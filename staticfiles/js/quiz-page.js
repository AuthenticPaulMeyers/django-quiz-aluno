// Timer Script
document.addEventListener('DOMContentLoaded', function () {
      const durationElement = document.querySelector('.js-duration');
      let duration = parseInt(durationElement.textContent) * 60; // Convert minutes to seconds

      // Check if there's saved time in localStorage
      const savedTime = localStorage.getItem('quizTimeRemaining');
      if (savedTime) {
            duration = parseInt(savedTime);
      }

      function updateTimer() {
            const minutes = Math.floor(duration / 60);
            const seconds = duration % 60;

            durationElement.textContent = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

            if (duration <= 0) {
                  clearInterval(timerInterval);
                  // TODO: Add a popup alert when the time is up and disable all quiz buttons
                  alert('Time is up! The quiz will be submitted automatically.');
                  document.querySelector('form').submit();
            }

            // save time to localstorage to avoid refresh reset
            localStorage.setItem('quizTimeRemaining', duration);

            duration--;
      }

      updateTimer(); // Initial call to display the timer immediately
      const timerInterval = setInterval(updateTimer, 1000);

      // Prevent Back Navigation
      history.pushState(null, null, location.href);
      window.onpopstate = function () {
            history.go(1);
      };

      // Auto-submit on Tab Close or Refresh
      window.addEventListener('unload', function () {
            navigator.sendBeacon(document.querySelector('form').action, new FormData(document.querySelector('form')));

      });
});

// Question Navigation Script
let currentQuestionIndex = 0;
const questionBlocks = document.querySelectorAll('.question-block');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const submitBtn = document.getElementById('submitBtn');

function showQuestion(index) {
      questionBlocks.forEach((block, i) => {
            block.classList.toggle('hidden', i !== index);
      });
      currentQuestionIndex = index;
      updateNavigationButtons();
}

function showNextQuestion() {
      if (currentQuestionIndex < questionBlocks.length - 1) {
            showQuestion(currentQuestionIndex + 1);
      }
}

function showPreviousQuestion() {
      if (currentQuestionIndex > 0) {
            showQuestion(currentQuestionIndex - 1);
      }
}

// Disable next button until an answer is selected
questionBlocks.forEach((block) => {
      const inputs = block.querySelectorAll('input[type="radio"]');
      inputs.forEach((input) => {
            input.addEventListener('change', () => {
                  nextBtn.disabled = false;
            });
      });
});

// // Disable previous button if on first question
// prevBtn.disabled = currentQuestionIndex === 0;

function updateNavigationButtons() {
      prevBtn.classList.toggle('hidden', currentQuestionIndex === 0);
      nextBtn.classList.toggle('hidden', currentQuestionIndex === questionBlocks.length - 1);
      submitBtn.classList.toggle('hidden', currentQuestionIndex !== questionBlocks.length - 1);
}

// Initialize the first question
showQuestion(0);

// Clear localStorage on form submission and attach remaining time to hidden field
document.querySelector('form').addEventListener('submit', function () {
      const timeField = document.querySelector('.js-time-remaining');
      const saved = localStorage.getItem('quizTimeRemaining');
      if (timeField) {
            timeField.value = saved ? saved : '';
      }
      localStorage.removeItem('quizTimeRemaining');
      localStorage.removeItem('quizAnswers');
});

// Fill progress bar and percentage
function updateProgress() {
      const totalQuestions = questionBlocks.length;
      const answeredQuestions = Array.from(questionBlocks).filter(block => {
            const inputs = block.querySelectorAll('input[type="radio"]');
            return Array.from(inputs).some(input => input.checked);
      }).length;

      const progressBar = document.querySelector('.js-progress-bar-fill');
      const progressPercentage = document.querySelector('.js-progress');

      if (totalQuestions > 0) {
            const percentage = (answeredQuestions / totalQuestions) * 100;
            progressBar.style.width = `${percentage}%`;
            progressPercentage.textContent = `${Math.round(percentage)}%`;
      }
}
// Update progress when next button is clicked
nextBtn.addEventListener('click', updateProgress);
// Update progress when previous button is clicked
prevBtn.addEventListener('click', updateProgress);
// Update progress when an answer is selected
document.querySelectorAll('input[type="radio"]').forEach(input => {
      input.addEventListener('change', updateProgress);
});

const form = document.querySelector("form");
const btn = document.getElementById("submitBtn");
const spinner = document.getElementById("loading-spinner");

form.addEventListener("submit", function () {
      btn.disabled = true;
      btn.classList.add("opacity-75", "cursor-not-allowed");
      spinner.classList.remove("hidden");
});