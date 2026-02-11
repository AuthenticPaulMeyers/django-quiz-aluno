window.addEventListener('DOMContentLoaded', (event) => {
      // clear localStorage on page load
      localStorage.removeItem('quizTimeRemaining');
      localStorage.removeItem('quizAnswers');

      // DOM elements inside the modal
      const modal = document.querySelector('#popup-modal');
      const spinner = document.querySelector('#loading-spinner');
      const startExamBtn = document.querySelector('.js-attempt-quiz-button');
      // prefer the form inside the modal if present
      const form = modal ? modal.querySelector('form') : document.querySelector('form');

      if (!form) return;

      // On submit: disable button, show spinner, and close the modal
      form.addEventListener('submit', function () {
            if (modal) {
                  modal.classList.add('hidden');
                  modal.setAttribute('aria-hidden', 'true');
            }

            // Add loading state to the start exam button
            if (startExamBtn) {
                  startExamBtn.disabled = true;
                  startExamBtn.classList.add("opacity-70", "cursor-not-allowed");
                  // Move spinner from continue button to start exam button
                  if (spinner) {
                        spinner.classList.remove("hidden");
                  }
            }
      });

});