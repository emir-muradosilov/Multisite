document.addEventListener('DOMContentLoaded', function () {
    console.log('lead.js загружен');
    const forms = document.querySelectorAll('.lead-form');
    console.log('Найдено форм:', forms.length);

    forms.forEach(function(form, index) {
        console.log(`Обработчик для формы #${index + 1}`);
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            console.log('Отправка формы #' + (index + 1));

            // Проверка чекбокса
            const policyCheck = form.querySelector('.policy-check');
            if (!policyCheck) {
                alert('Нет чекбокса согласия! Добавьте .policy-check');
                return;
            }
            if (!policyCheck.checked) {
                alert('Необходимо согласиться с политикой конфиденциальности и договором оферты');
                return;
            }

            const formData = new FormData(form);
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            try {
                const response = await fetch('/lead/create/', {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrfToken
                    }
                });

                const data = await response.json();
                console.log('Ответ сервера:', data);

                if (data.success) {
                    // Скрываем форму, показываем success
                    const wrapper = form.closest('.lead-form-wrapper');
                    if (wrapper) {
                        form.classList.add('d-none');
                        const successDiv = wrapper.querySelector('.lead-success');
                        if (successDiv) {
                            successDiv.classList.remove('d-none');
                        }
                    } else {
                        // Если нет wrapper, просто скрыть форму
                        form.style.display = 'none';
                        // найти success блок внутри родителя
                        const parent = form.parentNode;
                        const success = parent.querySelector('.lead-success');
                        if (success) success.classList.remove('d-none');
                    }
                } else {
                    // Показываем конкретную ошибку от сервера
                    let errorMsg = 'Ошибка отправки';
                    if (data.errors) {
                        // собираем все ошибки полей
                        const errs = Object.values(data.errors).flat().join('; ');
                        if (errs) errorMsg = errs;
                    } else if (data.error) {
                        errorMsg = data.error;
                    }
                    alert(errorMsg);
                }
            } catch (error) {
                console.error('Fetch error:', error);
                alert('Ошибка отправки. Проверьте подключение к интернету.');
            }
        });
    });
});