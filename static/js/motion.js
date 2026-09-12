/**
 * Subtle scroll reveals for editorial layouts.
 */
document.addEventListener('DOMContentLoaded', function () {
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const items = document.querySelectorAll('.motion-reveal');
    if (!items.length || !('IntersectionObserver' in window)) return;

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    items.forEach(function (el, i) {
        el.style.transitionDelay = Math.min(i * 0.06, 0.36) + 's';
        observer.observe(el);
    });
});
