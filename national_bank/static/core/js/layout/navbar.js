// navbar.js
(function() {
  'use strict';

  // DOM elements
  const header = document.querySelector('.main-header');
  const toggler = document.querySelector('.navbar-toggler');
  const navCollapse = document.querySelector('.navbar-collapse');
  const navLinks = document.querySelectorAll('.nav-link');
  const dropdownToggles = document.querySelectorAll('.dropdown-toggle'); // for future dropdowns
  const body = document.body;

  // State
  let menuOpen = false;

  // Helper functions
  function toggleMenu(force) {
    menuOpen = force !== undefined ? force : !menuOpen;
    if (menuOpen) {
      navCollapse.classList.add('show');
      toggler.setAttribute('aria-expanded', 'true');
      body.classList.add('menu-open');
    } else {
      navCollapse.classList.remove('show');
      toggler.setAttribute('aria-expanded', 'false');
      body.classList.remove('menu-open');
      // Also close any open dropdowns on mobile
      document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
        menu.classList.remove('show');
        const btn = menu.previousElementSibling;
        if (btn && btn.classList.contains('dropdown-toggle')) {
          btn.setAttribute('aria-expanded', 'false');
        }
      });
    }
  }

  function closeMenu() {
    if (menuOpen) toggleMenu(false);
  }

  // Handle dropdown toggles (mobile)
  function handleDropdownToggle(e) {
    if (window.innerWidth < 992) {
      e.preventDefault();
      const toggle = e.currentTarget;
      const dropdownMenu = toggle.nextElementSibling;
      if (dropdownMenu && dropdownMenu.classList.contains('dropdown-menu')) {
        const isOpen = dropdownMenu.classList.contains('show');
        // Close other dropdowns
        document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
          if (menu !== dropdownMenu) {
            menu.classList.remove('show');
            menu.previousElementSibling.setAttribute('aria-expanded', 'false');
          }
        });
        dropdownMenu.classList.toggle('show', !isOpen);
        toggle.setAttribute('aria-expanded', !isOpen);
      }
    }
  }

  // Scroll handler: add/remove scrolled class
  function handleScroll() {
    if (window.scrollY > 10) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  }

  // Click outside handler
  function handleClickOutside(e) {
    if (menuOpen && !header.contains(e.target)) {
      closeMenu();
    }
  }

  // Resize handler: reset mobile menu if screen becomes large
  function handleResize() {
    if (window.innerWidth >= 992 && menuOpen) {
      toggleMenu(false);
    }
    // Ensure no body scroll class when desktop
    if (window.innerWidth >= 992 && body.classList.contains('menu-open')) {
      body.classList.remove('menu-open');
    }
  }

  // Initialize
  function init() {
    if (!toggler || !navCollapse) return;

    // Set ARIA attributes
    toggler.setAttribute('aria-expanded', 'false');
    toggler.setAttribute('aria-label', 'Toggle navigation');

    // Event listeners
    toggler.addEventListener('click', (e) => {
      e.preventDefault();
      toggleMenu();
    });

    // Close menu when a nav link is clicked (mobile)
    navLinks.forEach(link => {
      link.addEventListener('click', (e) => {
        if (window.innerWidth < 992 && menuOpen) {
          closeMenu();
        }
      });
    });

    // Dropdown toggles (if any)
    dropdownToggles.forEach(toggle => {
      toggle.addEventListener('click', handleDropdownToggle);
    });

    // Scroll event
    window.addEventListener('scroll', handleScroll, { passive: true });

    // Click outside
    document.addEventListener('click', handleClickOutside);

    // Resize event
    window.addEventListener('resize', handleResize);

    // Initial scroll check
    handleScroll();
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();