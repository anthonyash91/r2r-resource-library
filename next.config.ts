import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // pdfkit loads .afm font files from disk at runtime; keep it out of the bundle.
  serverExternalPackages: ["pdfkit"],
};

export default nextConfig;
