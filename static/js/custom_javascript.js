/* Toggle Mobile Search Bar */
function setupMobileSearchOverlay(showBtnId, hideBtnId, overlayId) {
    const showBtn = document.getElementById(showBtnId);
    const hideBtn = document.getElementById(hideBtnId);
    const overlay = document.getElementById(overlayId);

    if (showBtn && hideBtn && overlay) {
    showBtn.addEventListener("click", () => {
        overlay.classList.remove("d-none");
        requestAnimationFrame(() => overlay.classList.add("show"));
    });

    hideBtn.addEventListener("click", () => {
        overlay.classList.remove("show");
        overlay.addEventListener("transitionend", function handler() {
        overlay.classList.add("d-none");
        overlay.removeEventListener("transitionend", handler);
      });
    });
    }
}
document.addEventListener('DOMContentLoaded', () => {
    setupMobileSearchOverlay("showMobileSearchBtn", "hideMobileSearchBtn", "mobileSearchOverlay");
});

/* Toggle Reply-To-Comment field */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.reply-toggle-button').forEach(btn => {
    btn.addEventListener('click', e => {
      const commentId = e.currentTarget.dataset.commentId;
      const replyForm = document.getElementById(`reply-form-${commentId}`);
      const editForm = document.getElementById(`edit-form-${commentId}`);
      const commentText = document.getElementById(`comment-text-${commentId}`);

      if (replyForm) {
        const isReplyVisible = replyForm.style.display === 'block';
        replyForm.style.display = isReplyVisible ? 'none' : 'block';

        // Hide the edit form if it's open
        if (editForm && editForm.style.display === 'block') {
          editForm.style.display = 'none';
        }

        // Restore comment text if it was hidden by edit mode
        if (commentText && commentText.classList.contains('d-none')) {
          commentText.classList.remove('d-none');
          commentText.classList.add('d-block');
        }
      }
    });
  });
});

/* Toggle Edit-Comment field */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.edit-toggle-button').forEach(btn => {
    btn.addEventListener('click', e => {
      const commentId = e.target.dataset.commentId;
      const form = document.getElementById(`edit-form-${commentId}`);
      const text = document.getElementById(`comment-text-${commentId}`);
      const textarea = document.getElementById(`edit-textarea-${commentId}`);
      const replyForm = document.getElementById(`reply-form-${commentId}`);

      // Pre-fill textarea with current text
      textarea.value = text.textContent.trim();

      const isEditVisible = form.style.display === 'block';
      form.style.display = isEditVisible ? 'none' : 'block';

      text.classList.toggle('d-none', !isEditVisible);
      text.classList.toggle('d-block', isEditVisible);

      // Hide reply form if visible
      if (replyForm && replyForm.style.display === 'block') {
        replyForm.style.display = 'none';
      }
    });
  });
});

/* Expand text-area element and show the button in its corner */
document.querySelectorAll('.expand-on-focus').forEach(textarea => {
  textarea.addEventListener('focus', () => {
    textarea.rows = 3;

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

/* Mobile Sidebar */
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('mobileSidebar');
    const body = document.body;
    if (!sidebar) return;

    let touchStartX = 0;
    let touchEndX = 0;
    // Minimum swipe distance in px
    const threshold = 50;

    function handleGesture() {
      // Show Sidebar on Left Swipe
      if (touchStartX - touchEndX > threshold) {
        sidebar.classList.add('show');
        body.classList.add('no-scroll');
      // Hide Sidebar on Right Swipe
      } else if (touchEndX - touchStartX > threshold) {
        sidebar.classList.remove('show');
        body.classList.remove('no-scroll');
      }
    }

    document.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
    });

    document.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    handleGesture();
    });
});

/* Duplicating sidebar content into the mobile sidebar */
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.getElementById('mobileSidebar');
    const originalSidebar = document.getElementById('right-sidebar');

    if (sidebar && originalSidebar) {
    const clonedContent = originalSidebar.cloneNode(true);

    // Remove problematic Bootstrap classes
    clonedContent.classList.remove('col-md-3', 'd-none', 'd-md-block', 'sticky-sidebar', 'post-card');

    // Clear old content and insert cloned HTML
    const contentContainer = sidebar.querySelector('.mobile-sidebar-content');
    contentContainer.innerHTML = '';
    contentContainer.appendChild(clonedContent);
    }
});