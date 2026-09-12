/**
 * Auth form enhancements: username check, password rules, toggles, reveal animations.
 */
document.addEventListener('DOMContentLoaded', function () {
    initUsernameCheck();
    initPasswordRules();
    initPasswordToggles();
    initAuthReveals();
    initAuthSubmitState();
});

var USERNAME_PATTERN = /^[a-zA-Z0-9]+$/;

function initPasswordToggles() {
    document.querySelectorAll('.password-field__toggle, .password-toggle').forEach(function (btn) {
        const targetId = btn.getAttribute('data-password-target');
        const input = document.getElementById(targetId);
        if (!input) return;

        btn.addEventListener('click', function () {
            const show = input.type === 'password';
            input.type = show ? 'text' : 'password';
            btn.setAttribute('aria-pressed', show ? 'true' : 'false');
            btn.setAttribute('aria-label', show ? 'Hide password' : 'Show password');
            const icon = btn.querySelector('i');
            if (icon) {
                icon.className = show ? 'fas fa-eye-slash' : 'fas fa-eye';
            }
        });
    });
}

function initAuthReveals() {
    document.querySelectorAll('.auth-reveal').forEach(function (el) {
        el.classList.add('is-visible');
    });
}

function initAuthSubmitState() {
    document.querySelectorAll('.auth-form').forEach(function (form) {
        form.addEventListener('submit', function () {
            const btn = form.querySelector('.btn-auth-submit');
            if (!btn || btn.disabled) return;
            btn.disabled = true;
            btn.classList.add('is-loading');
            const label = btn.querySelector('span');
            if (label) label.textContent = 'Please wait…';
        });
    });
}

function initUsernameCheck() {
    const usernameInput = document.querySelector('#id_username');
    const feedback = document.getElementById('username-feedback');
    const checkUrl = window.AUTH_CHECK_USERNAME_URL;
    if (!usernameInput || !feedback || !checkUrl) return;

    let timer = null;
    let lastValue = '';

    function setFeedback(message, type) {
        feedback.hidden = !message;
        feedback.textContent = message;
        feedback.className = 'field-feedback field-feedback--' + type;
        usernameInput.classList.toggle('is-valid', type === 'success');
        usernameInput.classList.toggle('is-invalid', type === 'error');
    }

    usernameInput.addEventListener('input', function () {
        const raw = usernameInput.value;
        const cleaned = raw.replace(/[^a-zA-Z0-9]/g, '');
        if (raw !== cleaned) {
            usernameInput.value = cleaned;
        }

        const value = cleaned.trim();
        if (value === lastValue) return;
        lastValue = value;
        clearTimeout(timer);

        if (!value) {
            setFeedback('', 'neutral');
            return;
        }
        if (!USERNAME_PATTERN.test(value)) {
            setFeedback('Username can only contain letters and numbers.', 'error');
            return;
        }
        if (value.length < 3) {
            setFeedback('Username must be at least 3 characters.', 'error');
            return;
        }

        feedback.hidden = false;
        feedback.textContent = 'Checking availability…';
        feedback.className = 'field-feedback field-feedback--neutral';

        timer = setTimeout(function () {
            fetch(checkUrl + '?username=' + encodeURIComponent(value), {
                headers: { 'Accept': 'application/json' },
            })
                .then(function (res) { return res.json(); })
                .then(function (data) {
                    setFeedback(data.message, data.available ? 'success' : 'error');
                })
                .catch(function () {
                    setFeedback('Could not check username right now. You can still try to sign up.', 'neutral');
                });
        }, 400);
    });
}

function initPasswordRules() {
    const passwordInput = document.querySelector('#id_password1, #id_new_password1');
    const hint = document.getElementById('password-length-hint');
    if (!passwordInput || !hint) return;

    function updateHint() {
        const ok = passwordInput.value.length >= 8;
        hint.classList.toggle('is-met', ok);
        passwordInput.classList.toggle('is-valid', ok);
        passwordInput.classList.toggle('is-invalid', passwordInput.value.length > 0 && !ok);
    }

    passwordInput.addEventListener('input', updateHint);
    updateHint();
}

