/**
 * News + comment reaction buttons (like/dislike).
 */
document.addEventListener('DOMContentLoaded', function () {
    initNewsReactions();
    initCommentReactions();
});

function getCsrfToken() {
    const input = document.querySelector('[name=csrfmiddlewaretoken]');
    return input ? input.value : '';
}

function setReactionBusy(buttons, busy) {
    buttons.forEach(function (btn) {
        if (!btn) return;
        btn.classList.toggle('is-loading', busy);
        btn.disabled = busy;
    });
}

function initNewsReactions() {
    const bar = document.querySelector('[data-reaction-bar="news"]');
    if (!bar) return;

    const newsId = bar.dataset.newsId;
    const loginUrl = bar.dataset.loginUrl;
    const likeBtn = bar.querySelector('[data-reaction="like"]');
    const dislikeBtn = bar.querySelector('[data-reaction="dislike"]');
    const likeCount = bar.querySelector('[data-count="likes"]');
    const dislikeCount = bar.querySelector('[data-count="dislikes"]');
    let busy = false;

    async function send(isLike) {
        if (busy) return;
        busy = true;
        setReactionBusy([likeBtn, dislikeBtn], true);
        try {
            const body = new URLSearchParams();
            body.set('is_like', isLike ? '1' : '0');
            const response = await fetch('/interactions/news/' + newsId + '/like/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Accept': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: body.toString(),
            });
            if (response.status === 401 || response.status === 403) {
                window.location.href = loginUrl;
                return;
            }
            if (!response.ok) throw new Error('Could not save your reaction.');
            const data = await response.json();
            likeCount.textContent = data.total_likes;
            dislikeCount.textContent = data.total_dislikes;
            likeBtn.classList.toggle('is-active', data.liked);
            dislikeBtn.classList.toggle('is-active', data.disliked);
            likeBtn.setAttribute('aria-pressed', data.liked ? 'true' : 'false');
            dislikeBtn.setAttribute('aria-pressed', data.disliked ? 'true' : 'false');
            likeBtn.classList.add('reaction-pop');
            dislikeBtn.classList.remove('reaction-pop');
            if (!isLike) {
                dislikeBtn.classList.add('reaction-pop');
                likeBtn.classList.remove('reaction-pop');
            }
            setTimeout(function () {
                likeBtn.classList.remove('reaction-pop');
                dislikeBtn.classList.remove('reaction-pop');
            }, 350);
        } catch (err) {
            bar.setAttribute('data-reaction-error', 'Could not save your reaction. Please try again.');
            setTimeout(function () { bar.removeAttribute('data-reaction-error'); }, 3000);
        } finally {
            busy = false;
            setReactionBusy([likeBtn, dislikeBtn], false);
        }
    }

    if (likeBtn) likeBtn.addEventListener('click', function () { send(true); });
    if (dislikeBtn) dislikeBtn.addEventListener('click', function () { send(false); });
}

function initCommentReactions() {
    document.querySelectorAll('[data-comment-reactions]').forEach(function (bar) {
        const commentId = bar.dataset.commentId;
        const loginUrl = bar.dataset.loginUrl;
        const likeBtn = bar.querySelector('[data-reaction="like"]');
        const dislikeBtn = bar.querySelector('[data-reaction="dislike"]');
        const likeCount = bar.querySelector('[data-count="likes"]');
        const dislikeCount = bar.querySelector('[data-count="dislikes"]');
        let busy = false;

        async function send(isLike) {
            if (busy) return;
            busy = true;
            setReactionBusy([likeBtn, dislikeBtn], true);
            try {
                const body = new URLSearchParams();
                body.set('is_like', isLike ? '1' : '0');
                const response = await fetch('/interactions/comments/' + commentId + '/like/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCsrfToken(),
                        'Accept': 'application/json',
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: body.toString(),
                });
                if (response.status === 401 || response.status === 403) {
                    window.location.href = loginUrl;
                    return;
                }
                if (!response.ok) throw new Error('Could not save your reaction.');
                const data = await response.json();
                likeCount.textContent = data.total_likes;
                dislikeCount.textContent = data.total_dislikes;
                likeBtn.classList.toggle('is-active', data.liked);
                dislikeBtn.classList.toggle('is-active', data.disliked);
            } catch (err) {
                bar.classList.add('reaction-group--error');
                setTimeout(function () { bar.classList.remove('reaction-group--error'); }, 2000);
            } finally {
                busy = false;
                setReactionBusy([likeBtn, dislikeBtn], false);
            }
        }

        if (likeBtn) likeBtn.addEventListener('click', function () { send(true); });
        if (dislikeBtn) dislikeBtn.addEventListener('click', function () { send(false); });
    });
}
