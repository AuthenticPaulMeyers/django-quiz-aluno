window.addEventListener('DOMContentLoaded', (event) => {
      // clear localStorage on page load
      localStorage.removeItem('quizTimeRemaining');
      localStorage.removeItem('quizAnswers');

      // DOM elements inside the modal
      const modal = document.querySelector('#popup-modal');
      const continueBtn = document.querySelector('#continue-button');
      const spinner = document.querySelector('#loading-spinner');
      // prefer the form inside the modal if present
      const form = modal ? modal.querySelector('form') : document.querySelector('form');

      if (!form) return;

      // On submit: disable button, show spinner, and close the modal
      form.addEventListener('submit', function () {
            if (continueBtn) {
                  continueBtn.disabled = true;
                  continueBtn.classList.add('opacity-70', 'cursor-not-allowed');
            }

            if (spinner) {
                  spinner.classList.remove('hidden');
            }

            if (modal) {
                  modal.classList.add('hidden');
                  modal.setAttribute('aria-hidden', 'true');
            }
      });

});