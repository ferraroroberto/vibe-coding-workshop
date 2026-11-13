/* ============================================================
   VIBE CODING PRESENTATION — SLIDE ENGINE
   ============================================================ */

const slides = document.querySelectorAll('.slide');
const total = slides.length;
let current = 0;
let isAnimating = false;

// ── Build dots ──────────────────────────────────────────────
const dotsContainer = document.getElementById('slide-dots');
slides.forEach((_, i) => {
  const dot = document.createElement('div');
  dot.className = 'dot' + (i === 0 ? ' active' : '');
  dot.addEventListener('click', () => goTo(i));
  dotsContainer.appendChild(dot);
});

// ── Core navigation ─────────────────────────────────────────
function goTo(index, direction = 'next') {
  if (isAnimating || index === current || index < 0 || index >= total) return;

  isAnimating = true;
  const prev = current;
  current = index;

  const exitClass = direction === 'next' ? 'exit-left' : 'exit-right';

  slides[prev].classList.add(exitClass);
  slides[prev].classList.remove('active');

  slides[current].style.transform = direction === 'next' ? 'translateX(60px)' : 'translateX(-60px)';
  slides[current].style.opacity = '0';
  slides[current].classList.add('active');

  requestAnimationFrame(() => {
    requestAnimationFrame(() => {
      slides[current].style.transform = '';
      slides[current].style.opacity = '';
    });
  });

  setTimeout(() => {
    slides[prev].classList.remove(exitClass);
    isAnimating = false;
  }, 480);

  updateUI();
}

function nextSlide() { goTo(current + 1, 'next'); }
function prevSlide() { goTo(current - 1, 'prev'); }

// ── Update UI elements ──────────────────────────────────────
function updateUI() {
  // Counter
  document.getElementById('slide-counter').textContent = `${current + 1} / ${total}`;

  // Buttons
  document.getElementById('btn-prev').disabled = current === 0;
  document.getElementById('btn-next').disabled = current === total - 1;

  // Progress bar
  const pct = total > 1 ? (current / (total - 1)) * 100 : 100;
  document.getElementById('progress-fill').style.width = pct + '%';

  // Dots
  document.querySelectorAll('.dot').forEach((dot, i) => {
    dot.classList.toggle('active', i === current);
  });

  // Scroll inner content to top
  const inner = slides[current].querySelector('.slide-inner');
  if (inner) inner.scrollTop = 0;
}

// ── Keyboard navigation ──────────────────────────────────────
document.addEventListener('keydown', (e) => {
  switch (e.key) {
    case 'ArrowRight':
    case 'ArrowDown':
    case ' ':
    case 'PageDown':
      e.preventDefault();
      nextSlide();
      break;
    case 'ArrowLeft':
    case 'ArrowUp':
    case 'PageUp':
      e.preventDefault();
      prevSlide();
      break;
    case 'Home':
      e.preventDefault();
      goTo(0, 'prev');
      break;
    case 'End':
      e.preventDefault();
      goTo(total - 1, 'next');
      break;
    default:
      // Number keys 1–9 for quick jump
      if (e.key >= '1' && e.key <= '9') {
        const target = parseInt(e.key) - 1;
        goTo(target, target > current ? 'next' : 'prev');
      }
  }
});

// ── Touch / swipe support ────────────────────────────────────
let touchStartX = 0;
let touchStartY = 0;

document.addEventListener('touchstart', (e) => {
  touchStartX = e.touches[0].clientX;
  touchStartY = e.touches[0].clientY;
}, { passive: true });

document.addEventListener('touchend', (e) => {
  const dx = e.changedTouches[0].clientX - touchStartX;
  const dy = e.changedTouches[0].clientY - touchStartY;

  if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 50) {
    if (dx < 0) nextSlide();
    else prevSlide();
  }
}, { passive: true });

// ── Init ─────────────────────────────────────────────────────
updateUI();
