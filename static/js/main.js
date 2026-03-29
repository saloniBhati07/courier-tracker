/* CourierTrack — Main JavaScript */

// ── SIDEBAR TOGGLE (mobile) ──────────────────────────────────
function toggleSidebar() {
  const sidebar = document.getElementById('sidebar');
  if (sidebar) sidebar.classList.toggle('open');
}

// Close sidebar when clicking outside (mobile)
document.addEventListener('click', function(e) {
  const sidebar = document.getElementById('sidebar');
  const toggle  = document.querySelector('.menu-toggle');
  if (sidebar && toggle && !sidebar.contains(e.target) && !toggle.contains(e.target)) {
    sidebar.classList.remove('open');
  }
});

// ── TOPBAR CLOCK ──────────────────────────────────────────────
function updateClock() {
  const el = document.getElementById('topbar-date');
  if (!el) return;
  const now = new Date();
  el.textContent = now.toLocaleDateString('en-US', {
    weekday: 'short', year: 'numeric', month: 'short', day: 'numeric'
  });
}
updateClock();

// ── AUTO-DISMISS FLASH MESSAGES ──────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.flash').forEach(function(el) {
    setTimeout(function() {
      el.style.transition = 'opacity .4s';
      el.style.opacity = '0';
      setTimeout(function() { el.remove(); }, 400);
    }, 4000);
  });
});
