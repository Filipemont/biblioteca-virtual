class PasswordUtil{

    static validatePassword(password) {
        const errors = [];
        const minLength = 8;
        const specialCharacters = /[!@#$%^&*(),.?":{}|<>]/;

        if (password.length < minLength) {
            errors.push('A senha deve ter pelo menos 8 caracteres.');
        }

        if (!/[A-Z]/.test(password)) {
            errors.push('A senha deve conter pelo menos uma letra maiúscula.');
        }

        if (!/[a-z]/.test(password)) {
            errors.push('A senha deve conter pelo menos uma letra minúscula.');
        }

        if (!/[0-9]/.test(password)) {
            errors.push('A senha deve conter pelo menos um número.');
        }

        if (!specialCharacters.test(password)) {
            errors.push('A senha deve conter pelo menos um caractere especial (!@#$%^&*()).');
        }

        return errors;
}
    static encryptPassword(password) {
        let encrypted = CryptoJS.SHA256(password);
        return encrypted.toString();
    }

}
export default PasswordUtil;