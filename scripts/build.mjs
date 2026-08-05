import { spawnSync } from "node:child_process";
import { existsSync, renameSync, rmSync } from "node:fs";
import { join } from "node:path";

const executable = process.platform === "win32" ? "npx.cmd" : "npx";
const result = spawnSync(executable, ["vinext", "build"], {
  cwd: process.cwd(),
  encoding: "utf8",
  shell: process.platform === "win32",
});

process.stdout.write(result.stdout ?? "");
process.stderr.write(result.stderr ?? "");

const output = `${result.stdout ?? ""}\n${result.stderr ?? ""}`;
const completedBeforeWindowsCleanupError =
  process.platform === "win32" &&
  output.includes("Build complete.") &&
  output.includes("UV_HANDLE_CLOSING");

const buildSucceeded = result.status === 0 || completedBeforeWindowsCleanupError;

if (buildSucceeded) {
  const assetPrefix = process.env.NEXT_PUBLIC_BASE_PATH?.replace(/^\/+|\/+$/g, "");

  // GitHub Pages supplies the public repository path itself. Vinext writes
  // prefixed assets into a nested directory, so flatten only that build output.
  if (assetPrefix) {
    const nestedAssets = join("dist", "client", assetPrefix, "_next");
    const publicAssets = join("dist", "client", "_next");

    if (existsSync(nestedAssets)) {
      rmSync(publicAssets, { recursive: true, force: true });
      renameSync(nestedAssets, publicAssets);
      rmSync(join("dist", "client", assetPrefix), { recursive: true, force: true });
    }
  }
}

if (completedBeforeWindowsCleanupError) {
  console.warn("Static export completed; ignored a vinext Windows shutdown assertion.");
}

process.exit(buildSucceeded ? 0 : (result.status ?? 1));
