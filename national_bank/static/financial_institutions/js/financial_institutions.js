document.addEventListener('DOMContentLoaded', () => {
    const filterButtons = document.querySelectorAll('#type-filters .btn');
    const institutionCards = document.querySelectorAll('.institution-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // 1. Reset button styles
            filterButtons.forEach(btn => {
                btn.classList.remove('active', 'btn-primary');
                btn.classList.add('btn-outline-primary');
            });

            // 2. Set clicked button to active
            button.classList.remove('btn-outline-primary');
            button.classList.add('active', 'btn-primary');

            // 3. Get the filter category
            const filterValue = button.getAttribute('data-filter');

            // 4. Show/Hide cards based on filter
            institutionCards.forEach(card => {
                // If "all" is selected, or if the card matches the specific filter
                if (filterValue === 'all' || card.getAttribute('data-type') === filterValue) {
                    card.style.display = 'block';
                    card.style.animation = 'fadeIn 0.4s ease-out forwards';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
});