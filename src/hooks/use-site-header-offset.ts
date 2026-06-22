"use client";

import { useEffect, useState } from "react";

function readHeaderHeight(): number {
  const header = document.querySelector("header");
  return header?.getBoundingClientRect().height ?? 80;
}

export function useSiteHeaderOffset(): number {
  const [offset, setOffset] = useState(80);

  useEffect(() => {
    const header = document.querySelector("header");
    if (!header) return;

    const update = () => {
      setOffset(readHeaderHeight());
    };

    update();
    const resizeObserver = new ResizeObserver(update);
    resizeObserver.observe(header);
    window.addEventListener("scroll", update, { passive: true });

    return () => {
      resizeObserver.disconnect();
      window.removeEventListener("scroll", update);
    };
  }, []);

  return offset;
}
