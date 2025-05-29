// Функция валидации имени (и фамилии)
function validateName(fieldId) {
    const input = document.getElementById(fieldId);
    const errorSpan = document.getElementById(`${fieldId}Error`);
    const value = input.value.trim();

    // Регулярное выражение: первая буква заглавная, остальные строчные, только буквы
    const nameRegex = /^[А-ЯA-Z][а-яa-z]+$/;

    if (!value) {
        errorSpan.textContent = 'Поле не может быть пустым';
        input.style.borderColor = '#dc3545';
        return false;
    } else if (!nameRegex.test(value)) {
        errorSpan.textContent = 'Только буквы, первая заглавная';
        input.style.borderColor = '#dc3545';
        return false;
    } else {
        errorSpan.textContent = '';
        input.style.borderColor = '#28a745';
        return true;
    }
}

// Функция валидации email
function validateEmail() {
    const input = document.getElementById('email');
    const errorSpan = document.getElementById('emailError');
    const value = input.value.trim();

    // Простая проверка email (должна содержать @ и точку)
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!value) {
        errorSpan.textContent = 'Поле не может быть пустым';
        input.style.borderColor = '#dc3545';
        return false;
    } else if (!emailRegex.test(value)) {
        errorSpan.textContent = 'Введите корректный email';
        input.style.borderColor = '#dc3545';
        return false;
    } else {
        errorSpan.textContent = '';
        input.style.borderColor = '#28a745';
        return true;
    }
}

// Функция валидации пароля
function validatePassword() {
    const input = document.getElementById('password');
    const errorSpan = document.getElementById('passwordError');
    const value = input.value.trim();

    const minLength = 6;
    const maxLength = 20;

    if (!value) {
        errorSpan.textContent = 'Поле не может быть пустым';
        input.style.borderColor = '#dc3545';
        return false;
    } else if (value.length < minLength || value.length > maxLength) {
        errorSpan.textContent = `Длина пароля от ${minLength} до ${maxLength} символов`;
        input.style.borderColor = '#dc3545';
        return false;
    } else {
        errorSpan.textContent = '';
        input.style.borderColor = '#28a745';
        return true;
    }
}

// Валидация при отправке формы
document.getElementById('loginForm').addEventListener('submit', function(event) {
    const isFirstNameValid = validateName('firstName');
    const isLastNameValid = validateName('lastName');
    const isEmailValid = validateEmail();
    const isPasswordValid = validatePassword();

    if (!isFirstNameValid || !isLastNameValid || !isEmailValid || !isPasswordValid) {
        event.preventDefault(); // Блокируем отправку формы
    }
});