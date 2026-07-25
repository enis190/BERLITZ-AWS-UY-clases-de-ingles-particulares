document.addEventListener("DOMContentLoaded", () => {
  const items = document.querySelectorAll(".reveal");

  const io = new IntersectionObserver(
    (entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is_visible");
          obs.unobserve(entry.target);
        }
      });
    },
    {
      root: null,
      threshold: 0.2,
      rootMargin: "0px 0px -20% 0px"
    }
  );

  items.forEach((el) => {
    // Si debe mostrarse al cargar, no usar observer
    if (el.classList.contains("reveal_on_load")) {
      requestAnimationFrame(() => {
        el.classList.add("is_visible");
      });
    } else {
      io.observe(el);
    }
  });
});
