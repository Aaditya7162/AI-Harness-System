document.addEventListener('DOMContentLoaded', function() {
    const message = document.getElementById('welcome-message');
    const button = document.getElementById('change-btn');
    const greetings = [
        'Welcome!',
        'Hello there!',
        'Greetings!',
        'Hi, friend!',
        'Salutations!'
    ];
    let index = 0;
    button.addEventListener('click', function() {
        index = (index + 1) % greetings.length;
        message.textContent = greetings[index];
    });
});
