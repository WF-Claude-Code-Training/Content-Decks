(function () {
  const slides = Array.from(document.querySelectorAll(".slide"));
  const counter = document.getElementById("slideCounter");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  let current = 0;

  const fragmentSelectors = [
    ".objectives-list > li",
    ".category-grid > .category-card",
    ".agenda-columns > .agenda-col",
    ".survey-box",
    ".code-block",
    ".bench-footnote"
  ];

  // Wrap each slide body in a card container so layout/styling is centralized in CSS.
  slides.forEach((slide) => {
    if (slide.firstElementChild && slide.firstElementChild.classList.contains("slide-card")) {
      return;
    }
    const card = document.createElement("div");
    card.className = "slide-card";
    while (slide.firstChild) {
      card.appendChild(slide.firstChild);
    }
    slide.appendChild(card);
  });

  function collectFragments(slide) {
    const fragments = [];
    const seen = new Set();

    // Keep quiz pacing as question -> answer per item.
    slide.querySelectorAll(".mcq-list > .mcq-item").forEach((item) => {
      if (!seen.has(item)) {
        seen.add(item);
        item.classList.add("fragment");
        fragments.push(item);
      }

      const answer = item.querySelector(".mcq-answer");
      if (answer && !seen.has(answer)) {
        seen.add(answer);
        answer.classList.add("fragment");
        fragments.push(answer);
      }
    });

    fragmentSelectors.forEach((selector) => {
      slide.querySelectorAll(selector).forEach((el) => {
        if (seen.has(el)) return;
        seen.add(el);
        el.classList.add("fragment");
        fragments.push(el);
      });
    });

    fragments.forEach((el, i) => {
      el.style.setProperty("--fragment-index", String(i));
    });

    return fragments;
  }

  const slideFragments = slides.map(collectFragments);
  const fragmentProgress = slideFragments.map(() => 0);

  function applyFragmentState(slideIndex) {
    const visibleCount = fragmentProgress[slideIndex];
    slideFragments[slideIndex].forEach((fragment, index) => {
      fragment.classList.toggle("is-visible", index < visibleCount);
    });
  }

  function render() {
    slides.forEach((s, i) => {
      s.classList.toggle("active", i === current);
      applyFragmentState(i);
    });
    counter.textContent = `${current + 1} / ${slides.length}`;
  }

  function next() {
    if (fragmentProgress[current] < slideFragments[current].length) {
      fragmentProgress[current] += 1;
      render();
      return;
    }

    current = Math.min(current + 1, slides.length - 1);
    render();
  }

  function prev() {
    if (fragmentProgress[current] > 0) {
      fragmentProgress[current] -= 1;
      render();
      return;
    }

    const nextIndex = Math.max(current - 1, 0);
    if (nextIndex !== current) {
      current = nextIndex;
      fragmentProgress[current] = slideFragments[current].length;
      render();
    }

  }

  // Click anywhere on a slide to advance (except when clicking nav buttons)
  slides.forEach((s) => s.addEventListener("click", (e) => {
    if (e.target.closest("a, button")) return;
    next();
  }));

  prevBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    prev();
  });

  nextBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    next();
  });

  document.addEventListener("keydown", (e) => {
    if (["ArrowRight", "ArrowDown", " ", "PageDown"].includes(e.key)) {
      e.preventDefault();
      next();
    } else if (["ArrowLeft", "ArrowUp", "PageUp"].includes(e.key)) {
      e.preventDefault();
      prev();
    }
  });

  render();
})();
