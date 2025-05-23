/* Show/Hide Reply-To-Comment field */
document.querySelectorAll('.reply-toggle-button').forEach(btn => {
    btn.addEventListener('click', e => {
      const commentId = e.target.dataset.commentId;
      const form = document.getElementById(`reply-form-${commentId}`);
      if (form.style.display === 'block') form.style.display = 'none';
      else form.style.display = 'block';
    });
});


