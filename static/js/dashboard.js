
document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll(".counter").forEach(counter => {

        const target = parseFloat(counter.dataset.target);
        const decimals = Number.isInteger(target) ? 0 : 1;

        let current = 0;
        const step = target / 60;

        function updateCounter() {

            current += step;

            if (current < target) {
                counter.innerText = current.toFixed(decimals);
                requestAnimationFrame(updateCounter);
            } else {
                counter.innerText = target.toFixed(decimals);
            }
        }

        updateCounter();

    });

});