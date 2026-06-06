document.addEventListener('DOMContentLoaded', function () {

    const searchInput = document.getElementById('citySearch');

    if (!searchInput) return;

    searchInput.addEventListener('keyup', function () {

        const value = this.value.toLowerCase();

        const cities = document.querySelectorAll('.city-item');

        cities.forEach(city => {

            const text = city.innerText.toLowerCase();

            if (text.includes(value)) {

                city.style.display = 'block';

            } else {

                city.style.display = 'none';

            }

        });

    });

});