document.addEventListener("DOMContentLoaded", function () {
    const maxStock = parseInt(document.getElementById('max-stock-value').dataset.maxStock);
    const input = document.querySelector('.quantity-input');
    const btnIncrease = document.querySelector('.increase-btn');
    const btnDecrease = document.querySelector('.decrease-btn');

    input.setAttribute("readonly", true);

    window.increaseQuantity = function () {
        let current = parseInt(input.value);
        if (current < maxStock) {
            input.value = current + 1;
        }
        updateButtons();
    };

    window.decreaseQuantity = function () {
        let current = parseInt(input.value);
        if (current > 1) {
            input.value = current - 1;
        }
        updateButtons();
    };

    function updateButtons() {
        const value = parseInt(input.value);
        btnIncrease.disabled = value >= maxStock;
        btnDecrease.disabled = value <= 1;
    }

    updateButtons();
});