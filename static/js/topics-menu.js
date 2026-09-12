/**
 * Topics dropdown — compact scroll panel with fade hints.
 */
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-topics-scroll]').forEach(initTopicsScroll);
});

function initTopicsScroll(scrollEl) {
    const wrap = scrollEl.closest('.topics-menu__scroll-wrap');
    if (!wrap) return;

    const fadeTop = wrap.querySelector('[data-topics-fade="top"]');
    const fadeBottom = wrap.querySelector('[data-topics-fade="bottom"]');

    function updateFades() {
        const atTop = scrollEl.scrollTop <= 6;
        const atBottom = scrollEl.scrollTop + scrollEl.clientHeight >= scrollEl.scrollHeight - 6;
        if (fadeTop) fadeTop.classList.toggle('is-hidden', atTop);
        if (fadeBottom) fadeBottom.classList.toggle('is-hidden', atBottom);
    }

    scrollEl.addEventListener('scroll', updateFades, { passive: true });
    window.addEventListener('resize', updateFades);
    updateFades();

    const menu = scrollEl.closest('.dropdown-menu');
    const parent = menu ? menu.closest('.dropdown') : null;
    if (parent) {
        parent.addEventListener('shown.bs.dropdown', updateFades);
    }
}
