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

// نمایش یا پنهان کردن فرم ریپلای
function toggleReplyForm(commentId) {
    const form = document.getElementById(`reply-form-${commentId}`);
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

// نمایش یا پنهان کردن فرم اضافه کردن کامنت
function toggleAddComment() {
    const form = document.getElementById('add-comment-form');
    form.style.display = form.style.display === 'none' ? 'block' : 'none';
}

document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("theme-toggle");
    const icon = toggleButton.querySelector("i");

    function updateIcon() {
        if (document.body.classList.contains("day-mode")) {
            icon.classList.remove("fa-moon");
            icon.classList.add("fa-sun");
        } else {
            icon.classList.remove("fa-sun");
            icon.classList.add("fa-moon");
        }
    }

    toggleButton.addEventListener("click", function () {
        document.body.classList.toggle("day-mode");
        document.body.classList.toggle("night-mode");
        updateIcon();
    });

    // Set initial icon
    updateIcon();
});
