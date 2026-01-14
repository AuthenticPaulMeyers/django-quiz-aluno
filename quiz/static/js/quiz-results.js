window.addEventListener("DOMContentLoaded", function(){
      // Disable buttons when they are clicked to avoid double clicking and overloading the server
      const backDashboardBtn = document.querySelector('.back-dashboard-btn')

      if(!backDashboardBtn) return 

      backDashboardBtn.addEventListener('click', function(e){
            e.preventDefault();

            backDashboardBtn.disabled = true;
      });

});