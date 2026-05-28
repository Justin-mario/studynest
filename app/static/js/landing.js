/* StudyNest landing animations — vanilla JS, no deps.
 *
 *   - cycles the verb pill in the hero illustration
 *   - reveals progress bars on scroll
 *   - replays the marker-sweep highlight every few seconds
 */
(function () {
  "use strict";

  /* ---------- Verb pill cycle ---------- */
  const verbs = [
    { verb: "EXPLAIN",  ao: "AO2", tier: "Apply",    color: "#2D5BFF" },
    { verb: "DESCRIBE", ao: "AO1", tier: "Recall",   color: "#0F7A4E" },
    { verb: "ANALYSE",  ao: "AO3", tier: "Evaluate", color: "#FF6A2C" },
    { verb: "EVALUATE", ao: "AO3", tier: "Evaluate", color: "#6B3CC1" },
    { verb: "JUSTIFY",  ao: "AO3", tier: "Evaluate", color: "#E5366E" },
  ];
  let i = 0;
  const pill = document.querySelector("[data-verb-pill]");
  const verbWord = document.querySelector("[data-verb-word]");
  const aoBadge = document.querySelector("[data-ao]");
  const tierBadge = document.querySelector("[data-tier]");

  function tick() {
    if (!pill) return;
    const d = verbs[i];
    pill.textContent = d.verb;
    pill.style.background = d.color;
    pill.classList.remove("verb-cycle-pill");
    void pill.offsetWidth;            // restart animation
    pill.classList.add("verb-cycle-pill");
    if (verbWord) verbWord.textContent = d.verb.toLowerCase();
    if (aoBadge) aoBadge.textContent = d.ao;
    if (tierBadge) tierBadge.textContent = d.tier;
    i = (i + 1) % verbs.length;
  }
  if (pill) {
    tick();
    setInterval(tick, 3200);
  }

  /* ---------- Reveal animated bars when in view ---------- */
  const bars = document.querySelectorAll(".bar.bar-anim");
  if ("IntersectionObserver" in window && bars.length) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.4 });
    bars.forEach((b) => io.observe(b));
  }

  /* ---------- Replay marker-sweep on a loop ---------- */
  const sweeps = document.querySelectorAll(".marker-sweep-loop");
  sweeps.forEach((el) => {
    setInterval(() => {
      el.classList.remove("marker-sweep");
      void el.offsetWidth;
      el.classList.add("marker-sweep");
    }, 5500);
  });
})();
