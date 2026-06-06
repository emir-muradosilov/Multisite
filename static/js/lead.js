document.addEventListener('DOMContentLoaded', function () {

    const form = document.getElementById('leadForm');

    if (!form) return;

    form.addEventListener('submit', async function (e) {

        e.preventDefault();

        // ПРОВЕРКА ЧЕКБОКСА

        const policyAccept = document.getElementById('policyAccept');

        if (!policyAccept.checked) {

            alert(
                'Необходимо согласиться с политикой конфиденциальности и договором оферты'
            );

            return;
        }

        const formData = new FormData(form);

        const csrfToken = document.querySelector(
            '[name=csrfmiddlewaretoken]'
        ).value;

        const response = await fetch('/lead/create/', {

            method: 'POST',

            body: formData,

            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': csrfToken
            }

        });

        const data = await response.json();

        if (data.success) {

            form.classList.add('d-none');

            document
                .getElementById('leadSuccess')
                .classList.remove('d-none');

        } else {

            alert(data.error || 'Ошибка отправки');

        }

    });

});