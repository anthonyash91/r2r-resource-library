"use client";

import { useEffect } from "react";

/**
 * Homepage scroll progress bar + header elevation — mirrors initScrollFx() §1 in
 * redesign/Road to Reentry - Homepage.dc.html.
 */
export function HomeScrollProgress() {
  useEffect(() => {
    const bar = document.createElement("div");
    bar.setAttribute("aria-hidden", "true");
    bar.className = "home-scroll-progress";
    document.body.appendChild(bar);

    const header = document.querySelector<HTMLElement>(".app-site-header");
    if (header) {
      header.classList.add("home-scroll-header");
    }

    let ticking = false;

    const update = () => {
      ticking = false;
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const pct = max > 0 ? (window.scrollY / max) * 100 : 0;
      bar.style.width = `${pct}%`;
      if (header) {
        header.dataset.scrolled = window.scrollY > 8 ? "true" : "false";
      }
    };

    const onScroll = () => {
      if (!ticking) {
        ticking = true;
        requestAnimationFrame(update);
      }
    };

    update();
    window.addEventListener("scroll", onScroll, { passive: true });

    return () => {
      window.removeEventListener("scroll", onScroll);
      bar.remove();
      if (header) {
        header.classList.remove("home-scroll-header");
        delete header.dataset.scrolled;
      }
    };
  }, []);

  return null;
}
