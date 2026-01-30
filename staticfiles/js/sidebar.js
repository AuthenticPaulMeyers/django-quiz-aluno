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

