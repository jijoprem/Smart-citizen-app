document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');

    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const phoneNumber = document.getElementById('login-phone').value;
        const password = document.getElementById('login-password').value;

        // Simulate a successful login (replace with actual authentication logic)
        if (/^\d{10}$/.test(phoneNumber) && password.length >= 6) {
            alert('Login successful!');
            // Redirect to the dashboard or another page after successful login
            window.location.href = 'dashboard.html'; // Replace 'dashboard.html' with the actual page
        } else {
            alert('Invalid credentials. Please enter valid phone number and password.');
        }
    });

    signupForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const phoneNumber = document.getElementById('signup-phone').value;
        const gmail = document.getElementById('signup-gmail').value;
        const password = document.getElementById('signup-password').value;

        // Simulate a successful signup (replace with actual registration logic)
        if (/^\d{10}$/.test(phoneNumber) && gmail.includes('@') && gmail.includes('.') && password.length >= 6) {
            alert('Sign-up successful!');
            // Redirect to the dashboard or another page after successful signup
            window.location.href = 'dashboard.html'; // Replace 'dashboard.html' with the actual page
        } else {
            alert('Invalid credentials. Please enter valid phone number, Gmail, and password.');
        }
    });
});
