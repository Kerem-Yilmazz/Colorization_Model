const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

document.getElementById("mainlogin").addEventListener("click", function () {
    alert("Login Successful");
    window.open("index.html", "_blank");
    window.close();
});

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("mainregister").addEventListener("click", function () {
        alert("Registration Successful");
        window.open("index.html", "_blank");
        window.close();
    });
});
