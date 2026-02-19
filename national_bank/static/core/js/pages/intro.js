// intro.js
// Intro page interactions (minimal – just for demonstration and future enhancements)

(function() {
  'use strict';

  // Optional: Add a subtle animation or log
  console.log('Intro page loaded – National Bank of Ethiopia');

  // ===== Header scroll shadow (optional) =====
  const header = document.querySelector('header');
  if (header) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 10) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  }

  // ===== Button click tracking (example for analytics) =====
  const buttons = document.querySelectorAll('.btn');
  buttons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const btnText = btn.innerText.trim();
      console.log(`Button clicked: ${btnText}`);
      // You could send an analytics event here
    });
  });

  // ===== Smooth scroll for anchor links (if any) =====
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
})();