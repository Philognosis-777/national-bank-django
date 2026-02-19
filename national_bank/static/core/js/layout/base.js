// base.js
// Global JavaScript for National Bank of Ethiopia
// Handles language switching, global UI state, and accessibility

(function() {
  'use strict';

  // ==================== LANGUAGE TOGGLER ====================
  // Switches between English and Amharic using data-en / data-am attributes
  const LANG_STORAGE_KEY = 'nbe_language';
  const langToggleBtn = document.getElementById('langToggle');

  // Get current language from localStorage or default to 'en'
  let currentLang = localStorage.getItem(LANG_STORAGE_KEY) || 'en';

  // Function to switch language
  function switchLanguage(lang) {
    if (lang !== 'en' && lang !== 'am') return;

    // Update HTML lang attribute and direction
    document.documentElement.lang = lang;
    document.documentElement.dir = lang === 'am' ? 'rtl' : 'ltr';

    // Update all elements with data-en and data-am
    const elements = document.querySelectorAll('[data-en][data-am]');
    elements.forEach(el => {
      const enText = el.getAttribute('data-en');
      const amText = el.getAttribute('data-am');
      el.textContent = lang === 'am' ? amText : enText;
    });

    // Update toggle button text if exists
    if (langToggleBtn) {
      const langSpan = langToggleBtn.querySelector('.lang-text');
      if (langSpan) {
        langSpan.textContent = lang === 'am' ? 'English' : 'አማርኛ';
      }
    }

    // Save preference
    localStorage.setItem(LANG_STORAGE_KEY, lang);
    currentLang = lang;

    // Dispatch custom event for other scripts to react
    window.dispatchEvent(new CustomEvent('languagechange', { detail: { language: lang } }));
  }

  // Initialize language
  switchLanguage(currentLang);

  // Add event listener to toggle button if exists
  if (langToggleBtn) {
    langToggleBtn.addEventListener('click', (e) => {
      e.preventDefault();
      const newLang = currentLang === 'en' ? 'am' : 'en';
      switchLanguage(newLang);
    });
  }

  // ==================== GLOBAL SCROLL HANDLER ====================
  // Adds 'scrolled' class to header when page is scrolled
  const header = document.querySelector('.main-header');
  if (header) {
    function handleScroll() {
      if (window.scrollY > 10) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    }
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll(); // initial check
  }

  // ==================== MOBILE MENU BODY LOCK ====================
  // Prevents body scroll when mobile menu is open (works with navbar.js)
  // This listens for a custom event or class changes
  const body = document.body;
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.attributeName === 'class') {
        if (body.classList.contains('menu-open')) {
          body.style.overflow = 'hidden';
        } else {
          body.style.overflow = '';
        }
      }
    });
  });
  observer.observe(body, { attributes: true });

  // ==================== PAGE-SPECIFIC BODY CLASS ====================
  // Already set in template via page-{{ page_name }}
  // Additional logic if needed

  // ==================== ACCESSIBILITY: SKIP LINK ====================
  // Add skip to main content link if not present
  if (!document.querySelector('.skip-to-content')) {
    const skipLink = document.createElement('a');
    skipLink.href = '#mainContent';
    skipLink.className = 'skip-to-content';
    skipLink.textContent = 'Skip to main content';
    document.body.insertBefore(skipLink, document.body.firstChild);
  }

  // ==================== UTILITY FUNCTIONS ====================
  // Expose global utilities if needed
  window.NBE = window.NBE || {};
  window.NBE.switchLanguage = switchLanguage;
  window.NBE.currentLang = () => currentLang;

  // ==================== INITIALIZATION ====================
  console.log('Base.js initialized. Current language:', currentLang);
})();