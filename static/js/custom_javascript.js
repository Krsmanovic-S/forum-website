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
document.querySelectorAll('.reply-toggle-button').forEach(btn => {
    btn.addEventListener('click', e => {
      const commentId = e.target.dataset.commentId;
      const form = document.getElementById(`reply-form-${commentId}`);

      if (form.style.display === 'block')
      {
        form.style.display = 'none';
      }
      else form.style.display = 'block';
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