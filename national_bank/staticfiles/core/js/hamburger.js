// ==============================
// HAMBURGER PAGE ONLY FEATURES
// ==============================

class HamburgerMenuHandler {
    constructor() {
        this.links = document.querySelectorAll('.menu-link');
        this.init();
    }

    init() {
        this.links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                alert(`Navigate to: ${link.textContent.trim()}`);
            });
        });
    }
}

class FooterHandler {
    constructor() {
        this.init();
    }

    init() {
        document.querySelectorAll('.footer-links a').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                alert(`Navigate to ${link.textContent}`);
            });
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new HamburgerMenuHandler();
    new FooterHandler();
});