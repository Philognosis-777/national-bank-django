// ==============================
// MAIN INITIALIZER (CRITICAL FIX)
// ==============================

document.addEventListener('DOMContentLoaded', () => {

    // Prevent double init protection
    if (window.__NBE_INIT__) return;
    window.__NBE_INIT__ = true;

    // Core systems (only once)
    if (window.NBE?.LanguageSwitcher) {
        window.languageSwitcher = new window.NBE.LanguageSwitcher();
    }

    if (window.NBE?.AdvancedHeader) {
        window.advancedHeader = new window.NBE.AdvancedHeader();
    }

    if (window.NBE?.BackToTop) {
        window.backToTop = new window.NBE.BackToTop();
    }

    console.log("NBE system initialized safely");
});