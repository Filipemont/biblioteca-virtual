function encryptPassword(password) {
    let encrypted = CryptoJS.SHA256(password);
    return encrypted.toString();
}
const formulario = document.getElementById('form-login')
const password = document.getElementById('password')
formulario.addEventListener('submit', function(e) {
    e.preventDefault();
    let fieldValue = password.value;
    let encryptedValue = encryptPassword(fieldValue) + 'A#';
    password.value = '*'.repeat(fieldValue.length);
    let hiddenField = document.createElement('input');
    hiddenField.type = 'hidden';
    hiddenField.name = password.name;
    hiddenField.value = encryptedValue;
    password.removeAttribute('name');
    formulario.appendChild(hiddenField);
    HTMLFormElement.prototype.submit.call(formulario);

});