document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;
    const themeToggle = document.getElementById('theme-toggle');
    const savedTheme = localStorage.getItem('theme') || 'day-mode';

    // اعمال تم ذخیره‌شده
    body.classList.add(savedTheme);
    themeToggle.textContent = savedTheme === 'day-mode' ? 'Night' : 'Day';

    // تغییر تم هنگام کلیک روی دکمه
    themeToggle.addEventListener('click', function () {
        const isDayMode = body.classList.contains('day-mode');

        if (isDayMode) {
            body.classList.replace('day-mode', 'night-mode');
            localStorage.setItem('theme', 'night-mode');
            this.textContent = 'Day';
        } else {
            body.classList.replace('night-mode', 'day-mode');
            localStorage.setItem('theme', 'day-mode');
            this.textContent = 'Night';
        }
    });
});
