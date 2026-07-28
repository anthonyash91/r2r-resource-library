import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Smaller runtime image for hosts like Render (free tier is 512MB).
  output: "standalone",
  // pdfkit loads .afm font files from disk at runtime; keep it out of the bundle.
  serverExternalPackages: ["pdfkit"],
};

export default nextConfig;
