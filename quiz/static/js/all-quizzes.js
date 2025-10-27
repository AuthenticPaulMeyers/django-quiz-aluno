// Quiz filter script
(function(){
const buttons = document.querySelectorAll('.js-filter-btn');
const rows = document.querySelectorAll('table tbody tr[data-status]');

function applyFilter(filter) {
rows.forEach(r => {
      if (!filter || filter === 'all') {
      r.style.display = '';
      return;
      }
      const status = r.getAttribute('data-status');
      r.style.display = (status === filter) ? '' : 'none';
});
}

buttons.forEach(b => {
b.addEventListener('click', function(){
      // toggle active visual state
      buttons.forEach(btn => {
      btn.classList.remove('bg-primary','text-white');
      btn.classList.add('bg-background-light');
      btn.setAttribute('aria-pressed','false');
      });
      this.classList.add('bg-primary','text-white');
      this.classList.remove('bg-background-light');
      this.setAttribute('aria-pressed','true');

      const filter = this.getAttribute('data-filter');
      applyFilter(filter);
      // persist last filter
      try { localStorage.setItem('quizzesFilter', filter); } catch(e){}
});
});

// apply persisted filter on load
try{
const saved = localStorage.getItem('quizzesFilter') || 'all';
const btn = Array.from(buttons).find(b => b.getAttribute('data-filter') === saved);
if (btn) btn.click(); else buttons[0].click();
} catch(e){ buttons[0].click(); }
})();