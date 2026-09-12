/**
 * nevox comments — composer UX, replies, char count.
 */
document.addEventListener('DOMContentLoaded', function () {
    initCommentComposer();
    initReplyToggles();
});

function initCommentComposer() {
    document.querySelectorAll('[data-comment-composer]').forEach(function (composer) {
        const textarea = composer.querySelector('[data-comment-input]');
        const counter = composer.querySelector('[data-char-count]');
        const max = parseInt(textarea.getAttribute('maxlength') || '2000', 10);

        function updateCount() {
            const len = textarea.value.length;
            if (counter) {
                counter.textContent = len + ' / ' + max;
                counter.classList.toggle('is-near-limit', len > max * 0.9);
            }
        }

        function autoGrow() {
            textarea.style.height = 'auto';
            textarea.style.height = Math.min(textarea.scrollHeight, 220) + 'px';
        }

        textarea.addEventListener('input', function () {
            updateCount();
            autoGrow();
        });

        textarea.addEventListener('focus', function () {
            composer.classList.add('is-focused');
            autoGrow();
        });

        textarea.addEventListener('blur', function () {
            if (!textarea.value.trim()) {
                composer.classList.remove('is-focused');
            }
        });

        updateCount();
    });
}

function initReplyToggles() {
    document.querySelectorAll('[data-reply-toggle]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const id = btn.getAttribute('data-reply-target');
            toggleReplyForm(id);
        });
    });

    document.querySelectorAll('[data-reply-cancel]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const id = btn.getAttribute('data-reply-cancel');
            toggleReplyForm(id, false);
        });
    });

    document.querySelectorAll('[data-edit-toggle]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const id = btn.getAttribute('data-edit-toggle');
            const form = document.getElementById('edit-form-' + id);
            const content = document.getElementById('comment-content-' + id);
            if (!form || !content) return;
            const open = form.hidden;
            form.hidden = !open;
            content.hidden = open;
        });
    });

    document.querySelectorAll('[data-edit-cancel]').forEach(function (btn) {
        btn.addEventListener('click', function () {
            const id = btn.getAttribute('data-edit-cancel');
            const form = document.getElementById('edit-form-' + id);
            const content = document.getElementById('comment-content-' + id);
            if (form) form.hidden = true;
            if (content) content.hidden = false;
        });
    });
}

function toggleReplyForm(commentId, forceOpen) {
    const form = document.getElementById('reply-form-' + commentId);
    const btn = document.querySelector('[data-reply-toggle][data-reply-target="' + commentId + '"]');
    if (!form) return;

    const open = typeof forceOpen === 'boolean' ? forceOpen : form.hidden;
    form.hidden = !open;

    if (btn) {
        btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }

    if (open) {
        const textarea = form.querySelector('textarea');
        if (textarea) {
            textarea.focus();
        }
    }
}
