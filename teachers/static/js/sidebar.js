// Teacher Sidebar toggle functionality
document.addEventListener('DOMContentLoaded', function() {
  const toggleBtn = document.getElementById('toggle-sidebar');
  const sidebar = document.getElementById('teacher-sidebar');
  const overlay = document.getElementById('sidebar-overlay');
  const mainContent = document.querySelector('main');

  if (toggleBtn && sidebar) {
    toggleBtn.addEventListener('click', function() {
      sidebar.classList.toggle('hidden');
      if (overlay) {
        overlay.classList.toggle('hidden');
      }
      // Add overflow-hidden on body to prevent scrolling when sidebar is open
      if (!sidebar.classList.contains('hidden')) {
        document.body.classList.add('overflow-hidden');
      } else {
        document.body.classList.remove('overflow-hidden');
      }
    });

    // Close sidebar when a link is clicked
    const sidebarLinks = sidebar.querySelectorAll('a');
    sidebarLinks.forEach(link => {
      link.addEventListener('click', function() {
        sidebar.classList.add('hidden');
        if (overlay) {
          overlay.classList.add('hidden');
        }
        document.body.classList.remove('overflow-hidden');
      });
    });

    // Close sidebar when clicking on overlay
    if (overlay) {
      overlay.addEventListener('click', function() {
        sidebar.classList.add('hidden');
        overlay.classList.add('hidden');
        document.body.classList.remove('overflow-hidden');
      });
    }

    // Close sidebar when clicking outside on mobile/tablet
    if (mainContent) {
      mainContent.addEventListener('click', function(e) {
        if (window.innerWidth < 1024 && !sidebar.classList.contains('hidden') && e.target !== toggleBtn && !toggleBtn.contains(e.target)) {
          sidebar.classList.add('hidden');
          if (overlay) {
            overlay.classList.add('hidden');
          }
          document.body.classList.remove('overflow-hidden');
        }
      });
    }
  }
});
