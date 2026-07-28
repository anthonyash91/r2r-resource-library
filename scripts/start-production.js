/**
 * Production start for Render and similar hosts.
 * Prefers Next.js standalone server when present; falls back to `next start`.
 */
const { spawn } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const port = String(process.env.PORT || 10000);
const hostname = "0.0.0.0";

process.env.PORT = port;
process.env.HOSTNAME = hostname;

const standaloneServer = path.join(__dirname, "..", ".next", "standalone", "server.js");

console.log(`[start] cwd=${process.cwd()} PORT=${port} HOSTNAME=${hostname}`);
console.log(`[start] standalone=${fs.existsSync(standaloneServer) ? "yes" : "no"}`);

let child;
if (fs.existsSync(standaloneServer)) {
  child = spawn(process.execPath, [standaloneServer], {
    stdio: "inherit",
    env: process.env,
    cwd: path.join(__dirname, "..", ".next", "standalone"),
  });
} else {
  const nextBin = path.join(
    path.dirname(require.resolve("next/package.json")),
    "dist",
    "bin",
    "next"
  );
  child = spawn(
    process.execPath,
    [nextBin, "start", "--hostname", hostname, "--port", port],
    { stdio: "inherit", env: process.env }
  );
}

child.on("exit", (code, signal) => {
  if (signal) {
    process.kill(process.pid, signal);
    return;
  }
  process.exit(code ?? 1);
});
