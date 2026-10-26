'use strict';
// Navigation remains visible if JavaScript is unavailable.
const menu = document.querySelector('.menu-button');
const nav = document.getElementById('main-nav');
if (menu && nav) {
  document.body.dataset.menuReady = '';
  menu.hidden = false;
  const narrow = matchMedia('(max-width: 800px)');
  function closeMenu(returnFocus = false) {
    menu.setAttribute('aria-expanded', 'false');
    nav.removeAttribute('data-open');
    if (returnFocus) menu.focus();
  }
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.toggleAttribute('data-open', open);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') closeMenu(true);
  });
  nav.addEventListener('click', event => {
    const link = event.target.closest('a');
    if (!link || !narrow.matches) return;
    closeMenu();
    if (link.hash && link.origin === location.origin && link.pathname === location.pathname) {
      const target = document.getElementById(link.hash.slice(1));
      if (target) { target.tabIndex = -1; target.focus({preventScroll:true}); }
    }
  });
  narrow.addEventListener('change', () => closeMenu());
}
// Only present when two or more approved photos have been added. Always manual.
const slider = document.querySelector('.photo-slider');
if (slider) {
  const slides = [...slider.querySelectorAll('.slide')];
  const controls = slider.querySelector('.slider-controls');
  if (slides.length > 1 && controls) {
    controls.hidden = false;
    slider.setAttribute('role', 'region');
    slider.setAttribute('aria-roledescription', 'carousel');
    let current = 0;
    function show(next) {
      current = (next + slides.length) % slides.length;
      slides.forEach((slide, index) => {
        slide.hidden = index !== current;
        slide.setAttribute('aria-label', `Photograph ${index + 1} of ${slides.length}`);
      });
      controls.querySelector('[data-position]').textContent = `${current + 1} / ${slides.length}`;
    }
    controls.querySelector('[data-prev]').addEventListener('click', () => show(current - 1));
    controls.querySelector('[data-next]').addEventListener('click', () => show(current + 1));
    slider.addEventListener('keydown', event => {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault(); show(current + (event.key === 'ArrowRight' ? 1 : -1));
      }
    });
    let start = null;
    slider.addEventListener('touchstart', event => {
      start = event.touches.length === 1 ? {x:event.touches[0].clientX,y:event.touches[0].clientY} : null;
    }, {passive:true});
    slider.addEventListener('touchcancel', () => { start = null; }, {passive:true});
    slider.addEventListener('touchend', event => {
      if (!start || !event.changedTouches.length) return;
      const dx=event.changedTouches[0].clientX-start.x, dy=event.changedTouches[0].clientY-start.y;
      if (Math.abs(dx)>50 && Math.abs(dx)>Math.abs(dy)*1.4) show(current + (dx<0 ? 1 : -1));
      start=null;
    }, {passive:true});
    show(0);
  }
}
