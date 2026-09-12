/**
 * Hero carousel — 5.5s slides, persists position across page visits.
 */
document.addEventListener('DOMContentLoaded', function () {
    const root = document.querySelector('.hero-carousel');
    if (!root) return;

    const slides = Array.from(root.querySelectorAll('.hero-carousel__slide'));
    const dots = Array.from(root.querySelectorAll('.hero-carousel__dot'));
    const prevBtn = root.querySelector('.hero-carousel__arrow--prev');
    const nextBtn = root.querySelector('.hero-carousel__arrow--next');
    const progress = root.querySelector('.hero-carousel__progress span');
    const intervalMs = parseInt(root.dataset.interval || '5500', 10);
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const storageKey = 'homeHeroCarousel';

    if (slides.length <= 1) return;

    let index = 0;
    let elapsed = 0;
    let tickTimer = null;

    function readState() {
        try {
            const raw = sessionStorage.getItem(storageKey);
            if (!raw) return;
            const data = JSON.parse(raw);
            index = Number.isInteger(data.index) ? data.index : 0;
            const away = Date.now() - (data.savedAt || Date.now());
            elapsed = (data.elapsed || 0) + away;
            while (elapsed >= intervalMs) {
                elapsed -= intervalMs;
                index = (index + 1) % slides.length;
            }
            index = ((index % slides.length) + slides.length) % slides.length;
        } catch (err) {
            index = 0;
            elapsed = 0;
        }
    }

    function writeState() {
        sessionStorage.setItem(storageKey, JSON.stringify({
            index: index,
            elapsed: elapsed,
            savedAt: Date.now(),
        }));
    }

    function applySlide() {
        slides.forEach(function (slide, i) {
            slide.classList.toggle('is-active', i === index);
        });
        dots.forEach(function (dot, i) {
            dot.classList.toggle('is-active', i === index);
            dot.setAttribute('aria-selected', i === index ? 'true' : 'false');
        });
        if (progress) {
            progress.style.width = Math.min(100, (elapsed / intervalMs) * 100) + '%';
        }
    }

    function stopTimers() {
        clearInterval(tickTimer);
        tickTimer = null;
    }

    function startTimers() {
        stopTimers();
        if (reducedMotion) return;

        const step = 100;
        tickTimer = setInterval(function () {
            elapsed += step;
            if (elapsed >= intervalMs) {
                elapsed = 0;
                index = (index + 1) % slides.length;
                applySlide();
            } else if (progress) {
                progress.style.width = Math.min(100, (elapsed / intervalMs) * 100) + '%';
            }
            writeState();
        }, step);
    }

    function goTo(nextIndex, resetElapsed) {
        index = ((nextIndex % slides.length) + slides.length) % slides.length;
        if (resetElapsed !== false) {
            elapsed = 0;
        }
        applySlide();
        writeState();
        startTimers();
    }

    readState();
    applySlide();
    startTimers();

    if (nextBtn) {
        nextBtn.addEventListener('click', function () {
            goTo(index + 1, true);
        });
    }
    if (prevBtn) {
        prevBtn.addEventListener('click', function () {
            goTo(index - 1, true);
        });
    }
    dots.forEach(function (dot) {
        dot.addEventListener('click', function () {
            goTo(parseInt(dot.dataset.index, 10), true);
        });
    });

    root.addEventListener('mouseenter', stopTimers);
    root.addEventListener('mouseleave', startTimers);

    root.addEventListener('keydown', function (event) {
        if (event.key === 'ArrowRight') {
            event.preventDefault();
            goTo(index + 1, true);
        } else if (event.key === 'ArrowLeft') {
            event.preventDefault();
            goTo(index - 1, true);
        }
    });
    root.setAttribute('tabindex', '0');

    window.addEventListener('pagehide', writeState);
    document.addEventListener('visibilitychange', function () {
        if (document.hidden) {
            writeState();
            stopTimers();
            return;
        }
        readState();
        applySlide();
        startTimers();
    });
});
