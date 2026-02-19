// footer.js
(function() {
  'use strict';

  // ===== FOOTER FUNCTIONALITY =====
  // (No interactive needed for footer, but we keep for future language toggle support)
  
  // ===== COIN NAVIGATION =====
  const coinNav = document.getElementById('coinNav');
  const coinIcon = document.querySelector('.coin-icon');
  
  if (coinNav && coinIcon) {
    let expanded = false;
    
    // Toggle on click for mobile/touch devices
    coinIcon.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      expanded = !expanded;
      if (expanded) {
        coinNav.classList.add('expanded');
      } else {
        coinNav.classList.remove('expanded');
      }
    });
    
    // Close when clicking outside
    document.addEventListener('click', (e) => {
      if (!coinNav.contains(e.target) && expanded) {
        coinNav.classList.remove('expanded');
        expanded = false;
      }
    });
    
    // Optional: close on escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && expanded) {
        coinNav.classList.remove('expanded');
        expanded = false;
      }
    });
    
    // For accessibility: allow keyboard activation
    coinIcon.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        coinIcon.click();
      }
    });
    
    // Set ARIA attributes
    coinIcon.setAttribute('role', 'button');
    coinIcon.setAttribute('tabindex', '0');
    coinIcon.setAttribute('aria-expanded', 'false');
    coinIcon.setAttribute('aria-label', 'Toggle navigation menu');
    
    // Update ARIA when expanded changes
    const observer = new MutationObserver(() => {
      const isExpanded = coinNav.classList.contains('expanded');
      coinIcon.setAttribute('aria-expanded', isExpanded);
    });
    observer.observe(coinNav, { attributes: true, attributeFilter: ['class'] });
  }

  // ===== LANGUAGE TOGGLE SUPPORT (optional stub) =====
  // This function can be called by a language toggle button
  // It switches text content based on data-en / data-am attributes
  window.switchLanguage = function(lang) {
    const elements = document.querySelectorAll('[data-en][data-am]');
    elements.forEach(el => {
      const enText = el.getAttribute('data-en');
      const amText = el.getAttribute('data-am');
      if (lang === 'am' && amText) {
        el.textContent = amText;
      } else if (lang === 'en' && enText) {
        el.textContent = enText;
      }
    });
  };

  // Optionally detect language from localStorage or cookie
  // (To be integrated with navbar language toggle)
})();