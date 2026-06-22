import { cn } from "@/lib/utils";

type HeroSurfaceOrbsVariant = "home" | "page" | "sticky";

interface HeroSurfaceOrbsProps {
  variant?: HeroSurfaceOrbsVariant;
  className?: string;
}

function HeroOrb({
  className,
  tint = "white",
}: {
  className?: string;
  tint?: "white" | "cyan" | "blue";
}) {
  const haloClass =
    tint === "cyan"
      ? "bg-teal-200/18"
      : tint === "blue"
        ? "bg-sky-300/16"
        : "bg-white/14";

  return (
    <div className={cn("absolute", className)}>
      <div className={cn("absolute inset-0 rounded-full blur-3xl sm:blur-[4.5rem]", haloClass)} />
      <div className="absolute inset-[24%] rounded-full bg-white/18 blur-2xl" />
    </div>
  );
}

export function HeroSurfaceOrbs({ variant = "page", className }: HeroSurfaceOrbsProps) {
  return (
    <div
      className={cn("pointer-events-none absolute inset-0 overflow-hidden", className)}
      aria-hidden="true"
    >
      {variant === "home" ? (
        <>
          <HeroOrb
            tint="blue"
            className="h-[20rem] w-[20rem] -bottom-28 -left-28 sm:h-[24rem] sm:w-[24rem] sm:-bottom-32 sm:-left-32"
          />
          <HeroOrb
            tint="cyan"
            className="h-[18rem] w-[18rem] -right-24 top-0 sm:h-[22rem] sm:w-[22rem] sm:-right-28 sm:top-2"
          />
          <HeroOrb
            tint="white"
            className="left-1/2 top-1/2 h-[26rem] w-[26rem] -translate-x-1/2 -translate-y-[40%] opacity-35"
          />
          <HeroOrb tint="blue" className="h-56 w-56 -left-16 -top-16 sm:h-64 sm:w-64" />
        </>
      ) : variant === "sticky" ? (
        <>
          <HeroOrb tint="blue" className="h-32 w-32 -bottom-16 -left-10" />
          <HeroOrb tint="cyan" className="h-28 w-28 -right-8 -top-8" />
        </>
      ) : (
        <>
          <HeroOrb
            tint="blue"
            className="h-56 w-56 -bottom-20 -left-20 sm:h-64 sm:w-64 sm:-bottom-24 sm:-left-24"
          />
          <HeroOrb
            tint="cyan"
            className="h-52 w-52 -right-16 top-0 sm:h-60 sm:w-60 sm:-right-20 sm:top-2"
          />
          <HeroOrb
            tint="white"
            className="left-1/2 top-1/2 h-72 w-72 -translate-x-1/2 -translate-y-1/2 opacity-30"
          />
        </>
      )}
    </div>
  );
}
