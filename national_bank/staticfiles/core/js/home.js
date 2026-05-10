// ==============================
// HOME PAGE ONLY
// ==============================

document.addEventListener('DOMContentLoaded', () => {

    // Stats animation
    const stats = document.querySelectorAll('.stat-item h3');

    const animate = (el, end) => {
        let start = 0;

        const step = () => {
            start += end / 60;
            if (start >= end) start = end;

            el.textContent = Math.floor(start) + (el.textContent.includes('%') ? '%' : '');

            if (start < end) requestAnimationFrame(step);
        };

        step();
    };

    const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animate(entry.target, parseInt(entry.target.textContent));
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    stats.forEach(s => observer.observe(s));
});