/* Show/Hide Reply-To-Comment field */
document.querySelectorAll('.reply-toggle-button').forEach(btn => {
    btn.addEventListener('click', e => {
      const commentId = e.target.dataset.commentId;
      const form = document.getElementById(`reply-form-${commentId}`);
      if (form.style.display === 'block') form.style.display = 'none';
      else form.style.display = 'block';
    });
});

/* Expand text-area element and show the button in its corner */
document.querySelectorAll('.expand-on-focus').forEach(textarea => {
  textarea.addEventListener('focus', () => {
    textarea.rows = 2;

    const submitButton = textarea.closest('form').querySelector('button[type="submit"]');
    if (submitButton) {
      submitButton.style.display = 'block';
    }
  });

  textarea.addEventListener('blur', () => {
    if (!textarea.value.trim()) {
      textarea.rows = 1;

      const submitButton = textarea.closest('form').querySelector('button[type="submit"]');
      if (submitButton) {
        submitButton.style.display = 'none';
      }
    }
  });
});
