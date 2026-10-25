# Registration embed layout

Updated 25 October 2026.

- The separate “Open registration in a new tab” link is removed.
- The existing notice, “Registration of interest only. No payment is taken.”,
  is immediately after the iframe, aligned to the left edge of its Submit button.
- The embed uses `alignLeft=1` and `dynamicHeight=1` and Tally's official embed script, loaded
  only when a visitor opens registration. It fits the content instead of
  retaining the initial 620px fallback height.
- Each edition still passes its own `colour` parameter. Switching colours
  reloads the shared iframe; reopening the same colour keeps its answers.

Tally's built-in Submit button is inside a cross-origin iframe. Placing text
directly inside its button wrapper requires custom CSS, which is gated by
Tally Pro on this account. A preview-only CSS experiment was cleared; no
Tally content or settings were changed. The public website therefore places
the notice directly beneath the auto-sized embedded form. Tally's own footer
can remain between its Submit button and the external notice.

Reference: https://tally.so/help/embed-your-form

Latest alignment correction: the notice uses the embed’s 8px horizontal inset
and a -10px top margin to reclaim its bottom padding, leaving a compact gap
beneath Submit. The iframe remains fully visible and auto-sized.
