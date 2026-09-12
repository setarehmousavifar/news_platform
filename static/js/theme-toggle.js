/**
 * Theme toggle + toasts. Cache-bust with base.html ?v= query.
 */
document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;
    const themeToggle = document.getElementById('theme-toggle');
    const savedTheme = localStorage.getItem('theme') || 'day-mode';

    body.classList.remove('day-mode', 'night-mode');
    body.classList.add(savedTheme);

    function syncThemeButton() {
        if (!themeToggle) return;
        let icon = themeToggle.querySelector('i');
        if (!icon) {
            themeToggle.textContent = '';
            icon = document.createElement('i');
            icon.setAttribute('aria-hidden', 'true');
            themeToggle.appendChild(icon);
        }
        const isDay = body.classList.contains('day-mode');
        icon.className = isDay ? 'fas fa-sun' : 'fas fa-moon';
        themeToggle.setAttribute('aria-label', isDay ? 'Switch to night mode' : 'Switch to day mode');
        themeToggle.setAttribute('aria-pressed', isDay ? 'false' : 'true');
        themeToggle.setAttribute('title', isDay ? 'Night mode' : 'Day mode');
    }

    syncThemeButton();

    if (themeToggle) {
        themeToggle.addEventListener('click', function () {
            const isDay = body.classList.contains('day-mode');
            body.classList.remove('day-mode', 'night-mode');
            body.classList.add(isDay ? 'night-mode' : 'day-mode');
            localStorage.setItem('theme', isDay ? 'night-mode' : 'day-mode');
            syncThemeButton();
        });
    }

    document.querySelectorAll('.toast').forEach(function (el) {
        if (typeof bootstrap === 'undefined' || !bootstrap.Toast) return;
        bootstrap.Toast.getOrCreateInstance(el).show();
    });
});

function toggleReplyForm(commentId) {
    const form = document.getElementById('reply-form-' + commentId);
    const trigger = document.querySelector('[data-reply-target="' + commentId + '"]');
    if (!form) return;
    const isHidden = form.hasAttribute('hidden');
    if (isHidden) {
        form.removeAttribute('hidden');
        if (trigger) trigger.setAttribute('aria-expanded', 'true');
        const field = form.querySelector('textarea, input');
        if (field) field.focus();
    } else {
        form.setAttribute('hidden', '');
        if (trigger) trigger.setAttribute('aria-expanded', 'false');
    }
}
