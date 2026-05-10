 document.addEventListener('DOMContentLoaded', function () {
            // ---------- LANGUAGE TOGGLE ----------
            const langBtn = document.getElementById('langToggle');
            const body = document.body;
            const langTextSpan = langBtn.querySelector('.lang-text');

            // Check local storage for saved language
            const savedLang = localStorage.getItem('nbe_lang');
            if (savedLang === 'am') {
                body.classList.add('lang-am');
                langTextSpan.textContent = 'English';
            } else {
                body.classList.remove('lang-am');
                langTextSpan.textContent = 'አማርኛ';
            }

            langBtn.addEventListener('click', function () {
                body.classList.toggle('lang-am');
                if (body.classList.contains('lang-am')) {
                    langTextSpan.textContent = 'English';
                    localStorage.setItem('nbe_lang', 'am');
                } else {
                    langTextSpan.textContent = 'አማርኛ';
                    localStorage.setItem('nbe_lang', 'en');
                }
            });

            // ---------- ACTIVE NAV LINK (based on current URL) ----------
            const currentPath = window.location.pathname;
            const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === currentPath) {
                    link.classList.add('active');
                }
            });

            // ---------- SMOOTH SCROLLING for anchor links ----------
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function (e) {
                    const href = this.getAttribute('href');
                    if (href === '#') return;
                    const target = document.querySelector(href);
                    if (target) {
                        e.preventDefault();
                        target.scrollIntoView({ behavior: 'smooth' });
                    }
                });
            });

            // ---------- COIN NAVIGATION EXPAND/COLLAPSE ----------
            const coinNav = document.getElementById('coinNav');
            const coinIcon = document.getElementById('coinIcon');
            let isExpanded = false;

            coinIcon.addEventListener('click', function (e) {
                e.stopPropagation();
                isExpanded = !isExpanded;
                if (isExpanded) {
                    coinNav.classList.add('expanded');
                } else {
                    coinNav.classList.remove('expanded');
                }
            });

            // Close coin nav when clicking outside
            document.addEventListener('click', function (event) {
                if (!coinNav.contains(event.target) && isExpanded) {
                    isExpanded = false;
                    coinNav.classList.remove('expanded');
                }
            });

            // ---------- FOOTER FADE-IN ON SCROLL ----------
            const footerElements = document.querySelectorAll('.fade-in');
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('visible');
                        observer.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.15 });

            footerElements.forEach(el => observer.observe(el));

            // ---------- STICKY NAVBAR SCROLL EFFECT (shadow enhancement) ----------
            window.addEventListener('scroll', function () {
                const header = document.querySelector('.main-header');
                if (window.scrollY > 10) {
                    header.style.boxShadow = '0 4px 20px rgba(0,51,102,0.1)';
                } else {
                    header.style.boxShadow = '0 2px 15px rgba(0,0,0,0.05)';
                }
            });
        });
   