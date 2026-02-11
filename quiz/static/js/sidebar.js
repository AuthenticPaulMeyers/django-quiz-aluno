// Sidebar toggle functionality
document.addEventListener('DOMContentLoaded', function() {
  const toggleBtn = document.getElementById('toggle-sidebar');
  const sidebar = document.getElementById('student-sidebar');
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

    // Close sidebar when clicking outside on mobile
    if (mainContent) {
      mainContent.addEventListener('click', function(e) {
        if (window.innerWidth < 640 && !sidebar.classList.contains('hidden') && e.target !== toggleBtn && !toggleBtn.contains(e.target)) {
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

// get all the nav items 
const navItems = document.querySelectorAll('.nav-items');
const currentNavItem = document.querySelector('#current-item');

navItems.forEach(item, function(e){
      e.preventDefaults()
      console.log(this)
      this.classList.add('text-primary')
      this.classList.add('bg-primary')
      currentNavItem.classList.remove('text-primary')
      currentNavItem.classList.remove('bg-primary')
});


