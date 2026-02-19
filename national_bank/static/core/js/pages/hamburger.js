// hamburger.js
// Page-specific JavaScript for the Hamburger Menu page
// Handles quick action button interactions and any menu-specific behavior

(function() {
  'use strict';

  // ===== Quick Action Buttons =====
  // These are placeholders for future functionality (e.g., modals, calculators)
  const quickActionBtns = document.querySelectorAll('.quick-action-btn');

  quickActionBtns.forEach(btn => {
    btn.addEventListener('click', function(e) {
      e.preventDefault();

      // Get button text for feedback (respect current language)
      const englishSpan = this.querySelector('.english');
      const amharicSpan = this.querySelector('.amharic');
      let actionName = '';

      // Determine which language is currently visible
      if (englishSpan && window.getComputedStyle(englishSpan).display !== 'none') {
        actionName = englishSpan.textContent.trim();
      } else if (amharicSpan && window.getComputedStyle(amharicSpan).display !== 'none') {
        actionName = amharicSpan.textContent.trim();
      }

      // Simulate action (in production, this would open a modal or navigate)
      console.log(`Quick action clicked: ${actionName}`);

      // Optional: Add a subtle feedback animation
      this.classList.add('clicked');
      setTimeout(() => {
        this.classList.remove('clicked');
      }, 200);

      // You could also trigger a custom event for analytics
      const event = new CustomEvent('quickAction', {
        detail: { action: actionName }
      });
      window.dispatchEvent(event);
    });

    // Add focus styles for accessibility
    btn.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        btn.click();
      }
    });
  });

  // ===== Menu Card Links (optional enhancement) =====
  // If you want to track card clicks or add analytics
  const menuLinks = document.querySelectorAll('.menu-link');
  menuLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      // Optional: log navigation for analytics
      const linkText = this.querySelector('.english')?.textContent || this.querySelector('.amharic')?.textContent;
      console.log(`Menu link clicked: ${linkText}`);
    });
  });

  // ===== Language Change Adaptation =====
  // Listen for language change events from base.js to update any dynamic content if needed
  window.addEventListener('languagechange', (e) => {
    const lang = e.detail.language;
    console.log(`Hamburger page detected language switch to: ${lang}`);
    // If you have any dynamic elements that need to update based on language,
    // you can handle them here. Currently, the bilingual spans are toggled by base.js.
  });

  // ===== Initialization =====
  console.log('Hamburger page JS loaded');
})();