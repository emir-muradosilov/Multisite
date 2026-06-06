document.addEventListener('DOMContentLoaded', function () {

    const phones = document.querySelectorAll(
        'input[name="phone"]'
    );

    phones.forEach(input => {

        input.addEventListener('input', function () {

            let value = input.value.replace(/\D/g, '');

            if (value.startsWith('8')) {
                value = '7' + value.slice(1);
            }

            if (!value.startsWith('7')) {
                value = '7' + value;
            }

            let formatted = '+7';

            if (value.length > 1) {
                formatted += ' (' + value.substring(1,4);
            }

            if (value.length >= 5) {
                formatted += ') ' + value.substring(4,7);
            }

            if (value.length >= 8) {
                formatted += '-' + value.substring(7,9);
            }

            if (value.length >= 10) {
                formatted += '-' + value.substring(9,11);
            }

            input.value = formatted;

        });

    });

});