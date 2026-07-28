export function HeroDecorativeShapes() {
  return (
    <div className="pointer-events-none absolute inset-0 overflow-hidden" aria-hidden="true">
      <div className="hero-shape-float-tri absolute left-[8%] top-[60px] h-0 w-0 border-x-[11px] border-b-[18px] border-x-transparent border-b-[#FFB35C] opacity-90 sm:left-[140px]" />
      <div className="hero-shape-float-a absolute right-[8%] top-12 h-[18px] w-[18px] rounded-full bg-[var(--coral)] opacity-90 sm:right-[150px]" />
      <div className="hero-shape-float-c absolute bottom-8 left-[6%] h-[26px] w-[26px] rounded-full border-[5px] border-primary opacity-70 sm:left-[90px]" />
      <svg
        className="hero-shape-float-b absolute bottom-10 right-[10%] sm:right-[110px]"
        width="46"
        height="18"
        viewBox="0 0 46 18"
        fill="none"
        stroke="#FF9D6C"
        strokeWidth="3"
        strokeLinecap="round"
        aria-hidden="true"
      >
        <path d="M2 14 L9 4 L16 14 L23 4 L30 14 L37 4 L44 14" />
      </svg>
      <div className="hero-shape-pulse absolute left-[20%] top-[150px] h-2 w-2 rounded-full bg-primary opacity-60 sm:left-[230px]" />
      <div className="hero-shape-pulse hero-shape-pulse-delay absolute right-[22%] top-[130px] h-2 w-2 rounded-full bg-[#FFB35C] opacity-80 sm:right-[250px]" />
      <div className="hero-shape-float-c absolute left-[28%] top-[186px] h-5 w-5 rounded-full border-4 border-[#FF9D6C] opacity-55 sm:left-[300px]" />
      <div className="hero-shape-pulse hero-shape-pulse-delay-2 absolute right-[30%] top-[92px] h-2.5 w-2.5 rounded-full bg-primary opacity-50 sm:right-[330px]" />
      <div className="hero-shape-float-a absolute left-[5%] top-[148px] h-4 w-4 rotate-[14deg] rounded-[5px] bg-[#FFB35C] opacity-60 sm:left-[64px]" />
      <svg
        className="hero-shape-float-b absolute bottom-[52px] left-[24%] sm:left-[286px]"
        width="40"
        height="16"
        viewBox="0 0 46 18"
        fill="none"
        stroke="var(--accent)"
        strokeWidth="3"
        strokeLinecap="round"
        aria-hidden="true"
      >
        <path d="M2 14 L9 4 L16 14 L23 4 L30 14 L37 4 L44 14" />
      </svg>
      <div className="hero-shape-float-tri absolute bottom-16 right-[18%] h-0 w-0 border-x-[9px] border-b-[15px] border-x-transparent border-b-[var(--coral)] opacity-60 sm:right-[196px]" />
      <div className="hero-shape-pulse hero-shape-pulse-delay-3 absolute right-[7%] top-[170px] h-2 w-2 rounded-full bg-[#FF9D6C] opacity-70 sm:right-[86px]" />
    </div>
  );
}
