document.addEventListener('DOMContentLoaded', function () {
    var loginForm = document.getElementById('login-form');
    var registrationForm = document.getElementById('registration-form');

    document.getElementById('show-register-form').addEventListener('click', function (e) {
        e.preventDefault();
        loginForm.style.display = 'none';
        registrationForm.style.display = 'block';
    });

    document.getElementById('show-login-form').addEventListener('click', function (e) {
        e.preventDefault();
        registrationForm.style.display = 'none';
        loginForm.style.display = 'block';
    });
});
