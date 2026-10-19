import "./style.css";
import "./drinking-prototype.js";

// A single feature can be explored by hover, keyboard focus, or tap.
const hotspots = [...document.querySelectorAll('[data-hotspot]')];
let openHotspot = null;
let pinnedHotspot = null;
let hideHotspotTimer;
let restoringHotspotFocus = false;
function closeHotspot(restoreFocus = false) {
  clearTimeout(hideHotspotTimer);
  const previous = openHotspot;
  for (const hotspot of hotspots) {
    hotspot.classList.remove('is-open');
    hotspot.querySelector('.feature-pin').setAttribute('aria-expanded', 'false');
    hotspot.querySelector('.feature-popover').hidden = true;
  }
  openHotspot = pinnedHotspot = null;
  if (restoreFocus && previous) {
    restoringHotspotFocus = true;
    previous.querySelector('.feature-pin').focus();
    restoringHotspotFocus = false;
  }
}
// Keep every feature panel inside the viewport, including edge pins 2 and 5.
function positionHotspot(hotspot) {
  const panel = hotspot.querySelector('.feature-popover');
  hotspot.classList.remove('popover-flipped');
  panel.style.setProperty('--popover-offset-x', '0px');
  panel.style.setProperty('--popover-offset-y', '0px');
  if (matchMedia('(max-width:1000px)').matches) return;
  const margin = 16;
  const viewportWidth = document.documentElement.clientWidth;
  const viewportHeight = window.innerHeight;
  let box = panel.getBoundingClientRect();
  if ((hotspot.classList.contains('hotspot-left') && box.left < margin) ||
      (hotspot.classList.contains('hotspot-right') && box.right > viewportWidth - margin)) {
    hotspot.classList.add('popover-flipped');
    box = panel.getBoundingClientRect();
  }
  const offsetX = Math.max(margin - box.left, Math.min(0, viewportWidth - margin - box.right));
  const offsetY = Math.max(margin - box.top, Math.min(0, viewportHeight - margin - box.bottom));
  panel.style.setProperty('--popover-offset-x', `${offsetX}px`);
  panel.style.setProperty('--popover-offset-y', `${offsetY}px`);
}
let hotspotPositionFrame;
function scheduleHotspotPosition() {
  if (!openHotspot || hotspotPositionFrame) return;
  hotspotPositionFrame = requestAnimationFrame(() => {
    hotspotPositionFrame = null;
    if (openHotspot) positionHotspot(openHotspot);
  });
}
window.addEventListener('resize', scheduleHotspotPosition);
window.addEventListener('scroll', scheduleHotspotPosition, {passive:true, capture:true});
function showHotspot(hotspot, pin = false) {
  clearTimeout(hideHotspotTimer);
  if (openHotspot !== hotspot) closeHotspot();
  openHotspot = hotspot;
  pinnedHotspot = pin ? hotspot : null;
  hotspot.classList.add('is-open');
  hotspot.querySelector('.feature-pin').setAttribute('aria-expanded', 'true');
  hotspot.querySelector('.feature-popover').hidden = false;
  positionHotspot(hotspot);
}
for (const hotspot of hotspots) {
  const button = hotspot.querySelector('.feature-pin');
  hotspot.addEventListener('pointerenter', (event) => {
    if (event.pointerType !== 'mouse') return;
    showHotspot(hotspot);
  });
  hotspot.addEventListener('pointerleave', () => {
    if (pinnedHotspot === hotspot || hotspot.contains(document.activeElement)) return;
    hideHotspotTimer = setTimeout(() => closeHotspot(), 180);
  });
  hotspot.addEventListener('focusin', () => {
    if (!restoringHotspotFocus && openHotspot !== hotspot) showHotspot(hotspot);
  });
  hotspot.addEventListener('focusout', (event) => {
    if (!hotspot.contains(event.relatedTarget) && pinnedHotspot !== hotspot) closeHotspot();
  });
  button.addEventListener('click', () => {
    if (pinnedHotspot === hotspot) closeHotspot();
    else showHotspot(hotspot, true);
  });
  hotspot.querySelector('.feature-close').addEventListener('click', () => closeHotspot(true));
}
document.addEventListener('pointerdown', (event) => {
  if (openHotspot && !openHotspot.contains(event.target)) closeHotspot();
});
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && openHotspot) { event.preventDefault(); closeHotspot(true); }
});

// Both scene gestures pause offscreen, when hidden, or with reduced motion.
const sceneVisual = document.querySelector('.product-scene-visual');
const motionToggle = document.querySelector('.scene-motion-toggle');
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
let sceneVisible = false;
let scenePaused = false;
let pageTurnTimer;
let finishTurnTimer;
let lampToggleTimer;
let lampChangeTimer;
let lampGestureTimer;
const canAnimateScene = () => sceneVisible && !scenePaused && !reducedMotion.matches && !document.hidden;
function stopSceneMotion() {
  for (const timer of [pageTurnTimer, finishTurnTimer, lampToggleTimer, lampChangeTimer, lampGestureTimer]) clearTimeout(timer);
  sceneVisual.classList.remove('is-turning', 'is-switching-light');
}
function schedulePageTurn() {
  clearTimeout(pageTurnTimer);
  if (!canAnimateScene()) return;
  pageTurnTimer = setTimeout(() => {
    sceneVisual.classList.add('is-turning');
    finishTurnTimer = setTimeout(() => {
      sceneVisual.classList.remove('is-turning');
      schedulePageTurn();
    }, 2250);
  }, 14000 + Math.random() * 16000);
}
function scheduleLampToggle() {
  clearTimeout(lampToggleTimer);
  if (!canAnimateScene()) return;
  lampToggleTimer = setTimeout(() => {
    sceneVisual.classList.add('is-switching-light');
    lampChangeTimer = setTimeout(() => sceneVisual.classList.toggle('lamp-off'), 650);
    lampGestureTimer = setTimeout(() => sceneVisual.classList.remove('is-switching-light'), 2200);
    scheduleLampToggle();
  }, 30000);
}
function restartSceneMotion() {
  stopSceneMotion();
  schedulePageTurn();
  scheduleLampToggle();
}
new IntersectionObserver(([entry]) => {
  const visible = entry.isIntersecting;
  if (sceneVisible === visible) return;
  sceneVisible = visible;
  restartSceneMotion();
}, {threshold:0.25}).observe(sceneVisual);
motionToggle.addEventListener('click', () => {
  scenePaused = !scenePaused;
  motionToggle.setAttribute('aria-pressed', String(scenePaused));
  motionToggle.textContent = scenePaused ? 'Play scene' : 'Pause scene';
  restartSceneMotion();
});
reducedMotion.addEventListener('change', () => {
  motionToggle.hidden = reducedMotion.matches;
  restartSceneMotion();
});
motionToggle.hidden = reducedMotion.matches;
document.addEventListener('visibilitychange', restartSceneMotion);

// Colour studies are a local preference; they do not place an order.
const colourButtons = [...document.querySelectorAll('[data-colour]')];
const colourStatus = document.getElementById('colour-status');
for (const button of colourButtons) {
  button.addEventListener('click', () => {
    for (const choice of colourButtons) choice.setAttribute('aria-pressed', String(choice === button));
    colourStatus.textContent = `Selected: ${button.dataset.colour}. Colour study No. ${button.dataset.colourNumber}.`;
  });
}

// Show the actual vector crest at an inspectable size.
const crestDialog = document.getElementById('crest-dialog');
const crestTrigger = document.querySelector('[data-open-crest]');
crestTrigger.addEventListener('click', () => crestDialog.showModal());
crestDialog.querySelector('[data-close-crest]').addEventListener('click', () => crestDialog.close());
crestDialog.addEventListener('click', (event) => {
  if (event.target !== crestDialog) return;
  const box = crestDialog.getBoundingClientRect();
  if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) crestDialog.close();
});
crestDialog.addEventListener('close', () => crestTrigger.focus());
