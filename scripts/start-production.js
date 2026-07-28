/**
 * Production start for Render and other hosts that inject PORT.
 * Avoids shell ${PORT} expansion quirks in npm scripts.
 */
const { spawn } = require("node:child_process");
const path = require("node:path");

const nextBin = path.join(
  path.dirname(require.resolve("next/package.json")),
  "dist",
  "bin",
  "next"
);
const port = String(process.env.PORT || 8080);

const child = spawn(
  process.execPath,
  [nextBin, "start", "--hostname", "0.0.0.0", "--port", port],
  { stdio: "inherit", env: process.env }
);

child.on("exit", (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal);
    return;
  }
  process.exit(code ?? 1);
});
