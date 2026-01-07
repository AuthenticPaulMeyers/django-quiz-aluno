document.addEventListener('DOMContentLoaded', function () {
      const container = document.getElementById('questions-container');
      const addButton = document.getElementById('add-question');
      const template = document.getElementById('question-template');
      let questionCount = 1;

      // Function to update question numbers
      function updateQuestionNumbers() {
            container.querySelectorAll('.question-section').forEach((section, index) => {
                  section.querySelector('h3').textContent = `Question ${index + 1}`;
            });
      }

      // Add new question
      addButton.addEventListener('click', () => {
            questionCount++;
            const baseIndex = (questionCount - 1) * 4;
            const newQuestion = template.content.cloneNode(true);

            // Update template placeholders
            const html = newQuestion.firstElementChild.innerHTML
                  .replace('{number}', questionCount)
                  .replace('{optionA}', baseIndex)
                  .replace('{optionB}', baseIndex + 1)
                  .replace('{optionC}', baseIndex + 2)
                  .replace('{optionD}', baseIndex + 3)
                  .replace('{qindex}', questionCount - 1);

            const div = document.createElement('div');
            div.className = 'question-section rounded-lg border border-border-light dark:border-border-dark bg-gray-200 dark:bg-content-dark p-6 mb-4';
            div.innerHTML = html;

            container.appendChild(div);

            // Add remove button functionality
            const removeBtn = div.querySelector('.remove-question');
            if (removeBtn) {
                  removeBtn.addEventListener('click', () => {
                        div.remove();
                        questionCount--;
                        reindexQuestions();
                  });
            }

            // Ensure all fields (names/values) stay consistent after adding
            reindexQuestions();
      });

      // Reindex all question fields (names, checkbox values, headings)
      function reindexQuestions() {
            const sections = container.querySelectorAll('.question-section');
            sections.forEach((section, index) => {
                  // update heading
                  const h3 = section.querySelector('h3');
                  if (h3) h3.textContent = `Question ${index + 1}`;

                  // update file input name
                  const fileInput = section.querySelector('.question-image-input');
                  if (fileInput) fileInput.name = `question_image_${index}`;

                  // update checkbox values
                  const base = index * 4;
                  const checkboxes = section.querySelectorAll('input[type="checkbox"]');
                  checkboxes.forEach((cb, i) => {
                        cb.value = base + i;
                  });
            });

            // Keep questionCount consistent with sections
            questionCount = sections.length || 1;
      }

      // Initial reindex to ensure names/values are correct
      reindexQuestions();

      // Form validation
      document.querySelector('form').addEventListener('submit', function (e) {
            const questions = document.querySelectorAll('.question-section');
            let valid = true;

            questions.forEach(question => {
                  const checkboxes = question.querySelectorAll('input[type="checkbox"]');
                  const checked = Array.from(checkboxes).some(cb => cb.checked);
                  if (!checked) {
                        e.preventDefault();
                        valid = false;
                  }
            });

            if (!valid) {
                  alert('Each question must have at least one correct answer selected.');
            }
      });

      // Form submission loading state
      const form = document.querySelector('form');
      const createBtn = document.getElementById('create-quiz-btn');
      const quizSpinner = document.getElementById('quiz-spinner');
      const quizText = document.querySelector(".quiz-text")

      form.addEventListener('submit', function (e) {
            setTimeout(() => {
                  if (!e.defaultPrevented) {
                        createBtn.disabled = true;
                        createBtn.classList.add('opacity-75', 'cursor-not-allowed');
                        quizSpinner.classList.remove('hidden');
                        quizText.classList.add('hidden');
                  }
            }, 0);
      });

});