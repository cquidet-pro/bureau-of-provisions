import "./style.css";

// Filter the printed dispatch cards; the complete gallery also works without JS.
const filters = [...document.querySelectorAll("[data-city]")];
const cards = [...document.querySelectorAll(".dispatch-card")];
const count = document.querySelector(".gallery-count");
for (const button of filters) {
  button.addEventListener("click", () => {
    for (const filter of filters) filter.setAttribute("aria-pressed", String(filter === button));
    let visible = 0;
    for (const card of cards) {
      card.hidden = button.dataset.city !== "all" && card.dataset.location !== button.dataset.city;
      if (!card.hidden) visible++;
    }
    count.textContent = `${visible} ${visible === 1 ? "dispatch" : "dispatches"}`;
  });
}

// Native dialog supplies focus containment and Escape; image links remain the fallback.
const dialog = document.querySelector(".photo-dialog");
const photo = document.querySelector("#dialog-image");
const caption = document.querySelector("#dialog-caption");
let activeLinks = [];
let activeIndex = 0;
let opener;
function showPhoto(index) {
  activeIndex = (index + activeLinks.length) % activeLinks.length;
  const link = activeLinks[activeIndex];
  photo.src = link.href;
  photo.alt = link.querySelector("img").alt;
  caption.textContent = link.dataset.caption;
}
for (const link of document.querySelectorAll("[data-photo]")) {
  link.addEventListener("click", (event) => {
    if (typeof dialog.showModal !== "function" || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    activeLinks = cards.filter((card) => !card.hidden).map((card) => card.querySelector("a"));
    opener = link;
    showPhoto(activeLinks.indexOf(link));
    dialog.showModal();
  });
}
dialog.querySelector("[data-close]").addEventListener("click", () => dialog.close());
dialog.querySelector("[data-prev]").addEventListener("click", () => showPhoto(activeIndex - 1));
dialog.querySelector("[data-next]").addEventListener("click", () => showPhoto(activeIndex + 1));
dialog.addEventListener("keydown", (event) => {
  if (event.key === "ArrowLeft") { event.preventDefault(); showPhoto(activeIndex - 1); }
  if (event.key === "ArrowRight") { event.preventDefault(); showPhoto(activeIndex + 1); }
});
dialog.addEventListener("click", (event) => { if (event.target === dialog) dialog.close(); });
dialog.addEventListener("close", () => opener?.focus());

// Keep stable preference IDs in local storage and carry them to registration.
// Tally must be configured with cap_type and cap_label hidden fields to store them.
const CAP_KEY = "bop_cap_type";
const capInputs = [...document.querySelectorAll('input[name="cap_type"]')];
const capStatus = document.querySelector("#cap-picker-status");
const frame = document.querySelector("iframe[data-tally-src]");
const fallback = document.querySelector(".form-fallback a");
const registrationButton = document.querySelector("#start-registration");
const registrationStatus = document.querySelector("#registration-preference");
let formPreference;
let formStarted = false;
let embedScriptLoaded = false;

function selectedCap() {
  return capInputs.find((input) => input.checked) ?? null;
}

function preferenceUrl(base) {
  const url = new URL(base, window.location.href);
  const chosen = selectedCap();
  if (chosen) {
    url.searchParams.set("cap_type", chosen.value);
    url.searchParams.set("cap_label", chosen.dataset.label);
  } else {
    url.searchParams.delete("cap_type");
    url.searchParams.delete("cap_label");
  }
  return url.toString();
}

function updatePreference() {
  const chosen = selectedCap();
  capStatus.textContent = chosen ? `Selected: ${chosen.dataset.name}.` : "No lid preference selected.";
  fallback.href = preferenceUrl("https://tally.so/r/5BW7JN");
  if (!formStarted) return;
  const changed = formPreference !== (chosen?.value ?? "");
  registrationButton.hidden = !changed;
  registrationButton.textContent = "Start a new form with this preference ↗";
  registrationStatus.textContent = changed
    ? "Your open form keeps its previous lid preference. Starting a new form uses your latest choice and clears any answers already entered."
    : `Form preference: ${chosen?.dataset.name ?? "none selected"}.`;
}

// A valid deep link takes priority; ignore invalid values and retain a saved choice.
const capFromUrl = new URLSearchParams(window.location.search).get("cap");
let capFromStore;
try { capFromStore = window.localStorage.getItem(CAP_KEY); } catch { /* Storage is optional. */ }
const initial = capInputs.find((input) => input.value === capFromUrl)
  ?? capInputs.find((input) => input.value === capFromStore);
if (initial) initial.checked = true;
for (const input of capInputs) {
  input.addEventListener("change", () => {
    if (!input.checked) return;
    try { window.localStorage.setItem(CAP_KEY, input.value); } catch { /* Storage is optional. */ }
    // Keep the current page URL in step with the choice, including existing deep links.
    const url = new URL(window.location.href);
    url.searchParams.set("cap", input.value);
    window.history.replaceState(null, "", url);
    updatePreference();
  });
}
updatePreference();

// Snapshot the preference when the visitor opens the form. Radio changes never
// reload it; restarting requires an explicit click with the clearing notice visible.
registrationButton.addEventListener("click", () => {
  formPreference = selectedCap()?.value ?? "";
  formStarted = true;
  frame.closest(".register-embed").hidden = false;
  frame.src = preferenceUrl(frame.dataset.tallySrc);
  if (!embedScriptLoaded) {
    embedScriptLoaded = true;
    const script = document.createElement("script");
    script.src = "https://tally.so/widgets/embed.js";
    script.async = true;
    script.onload = () => window.Tally?.loadEmbeds();
    document.head.append(script);
  }
  updatePreference();
});

// Scrubbing a lid animation never changes its registration preference.
const motionControls = [...document.querySelectorAll("[data-motion]")];
const motionManifest = fetch("/images/lids/motion-clear/manifest.json").then((response) => {
  if (!response.ok) throw new Error("Lid animation unavailable");
  return response.json();
});
for (const control of motionControls) {
  const slug = control.dataset.motion;
  const frameRoot = control.dataset.motionPath || "/images/lids/motion-clear";
  const slider = control.querySelector("input");
  const output = control.querySelector("output");
  const image = document.getElementById(`${slug}-image`);
  const overlay = document.querySelector(`[data-motion-callouts="${slug}"]`);
  const frames = new Map();
  let request = 0;
  const loadFrame = (frame) => {
    if (!frames.has(frame)) {
      const photo = new Image();
      const ready = new Promise((resolve, reject) => {
        photo.onload = () => resolve(photo);
        photo.onerror = () => reject(new Error("Frame unavailable"));
      }).catch((error) => {
        frames.delete(frame);
        throw error;
      });
      photo.src = `${frameRoot}/${slug}/${String(frame).padStart(2, "0")}.webp`;
      frames.set(frame, ready);
    }
    return frames.get(frame);
  };
  const showFrame = async () => {
    const currentRequest = ++request;
    const frame = Number(slider.value);
    const pose = frame < 45 ? `Straw at ${45 + frame * 3} degrees` : frame === 45 ? "Straw folded flat at 180 degrees" : "Spray in action";
    slider.setAttribute("aria-valuetext", pose);
    output.value = frame > 45 ? "Spraying" : `${45 + frame * 3}°`;
    slider.style.setProperty("--progress", `${frame / Number(slider.max) * 100}%`);
    try {
      const [photo, manifest] = await Promise.all([loadFrame(frame), motionManifest]);
      await photo.decode();
      if (currentRequest !== request) return;
      image.src = photo.src;
      image.alt = `${control.querySelector("label").textContent.replace(" animation", "")}: ${pose.toLowerCase()}, drinking parts labelled`;
      const features = manifest[slug].annotations[frame];
      for (const line of overlay.querySelectorAll("[data-feature]")) {
        const point = features[line.dataset.feature];
        if (point) {
          const points = line.getAttribute("points").split(" ");
          points[points.length - 1] = point.join(",");
          line.setAttribute("points", points.join(" "));
        }
      }
    } catch {
      if (currentRequest !== request) return;
      output.value = "Preview unavailable";
    }
  };
  slider.addEventListener("input", showFrame);
  showFrame();
  // Fetch nearby cards' frames ahead of dragging, without loading them at the top of the page.
  const observer = new IntersectionObserver(async (entries) => {
    if (!entries.some((entry) => entry.isIntersecting)) return;
    observer.disconnect();
    const queue = Array.from({ length: Number(slider.max) + 1 }, (_, frame) => frame);
    await Promise.all(Array.from({ length: 3 }, async () => {
      while (queue.length) await loadFrame(queue.shift()).catch(() => {});
    }));
  }, { rootMargin: "300px" });
  observer.observe(control);
}
