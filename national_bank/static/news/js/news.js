// ==============================
// NEWS PAGE FILTER SYSTEM
// ==============================

document.addEventListener('DOMContentLoaded', () => {

    const buttons = document.querySelectorAll('.filter-btn');
    const cards = document.querySelectorAll('.news-card');

    function filter(category) {
        cards.forEach(card => {
            const match = category === 'all' || card.dataset.category === category;
            card.style.display = match ? 'flex' : 'none';
        });
    }

    buttons.forEach(btn => {
        btn.addEventListener('click', () => {
            buttons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            filter(btn.dataset.filter);
        });
    });

    filter('all');
});