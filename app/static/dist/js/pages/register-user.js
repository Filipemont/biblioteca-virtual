import PasswordUtil from "../validate-password-util.js";

const formulario = document.getElementById('form-register')
const password = document.getElementById('password')
const confirmPassword = document.getElementById('confirm_password')
formulario.addEventListener('submit', function (e) {
    e.preventDefault();
    let passwordFieldValue = password.value;
    let confirmPasswordFieldValue = confirmPassword.value;
    const errorPasswordMessages = PasswordUtil.validatePassword(passwordFieldValue);
    const errorPasswordDisplay = document.getElementById('errorPasswordMessages');
    errorPasswordDisplay.innerHTML = '';
    if (errorPasswordMessages.length > 0) {
        errorPasswordDisplay.innerHTML = errorPasswordMessages.join('<br>');
        return 0;
    }
    let encryptedPasswordValue = PasswordUtil.encryptPassword(passwordFieldValue) + 'A#';
    let encryptedConfirmPasswordValue = PasswordUtil.encryptPassword(confirmPasswordFieldValue) + 'A#';
    password.value = '*'.repeat(passwordFieldValue.length);
    confirmPassword.value = '*'.repeat(confirmPasswordFieldValue.length);
    let hiddenPasswordField = document.createElement('input');
    hiddenPasswordField.type = 'hidden';
    hiddenPasswordField.name = password.name;
    hiddenPasswordField.value = encryptedPasswordValue;

    let hiddenConfirmPasswordField = document.createElement('input');
    hiddenConfirmPasswordField.type = 'hidden';
    hiddenConfirmPasswordField.name = confirmPassword.name;
    hiddenConfirmPasswordField.value = encryptedConfirmPasswordValue;

    password.removeAttribute('name');
    confirmPassword.removeAttribute('name');

    formulario.appendChild(hiddenPasswordField);
    formulario.appendChild(hiddenConfirmPasswordField);

    HTMLFormElement.prototype.submit.call(formulario);
});
