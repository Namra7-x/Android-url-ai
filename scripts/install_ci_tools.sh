#!/usr/bin/env bash
set -euo pipefail

TOOLS_DIR="${RUNNER_TEMP:-/tmp}/android-url-atlas-tools"
CARGO_ROOT="$TOOLS_DIR/cargo"
mkdir -p "$TOOLS_DIR" "$CARGO_ROOT"

export DEBIAN_FRONTEND=noninteractive
sudo apt-get update
sudo apt-get install -y curl jq unzip zip xz-utils p7zip-full file binutils cargo rustc pkg-config libssl-dev

# Build the pinned apkeep version from crates.io. This avoids the GitHub
# release-asset CDN that repeatedly returned HTTP 504 in the previous runs.
export CARGO_NET_RETRY=8
export CARGO_HTTP_TIMEOUT=600
cargo install --locked --version 1.1.0 apkeep --root "$CARGO_ROOT" --force
APKEEP_BIN="$CARGO_ROOT/bin/apkeep"
test -x "$APKEEP_BIN"
echo "$CARGO_ROOT/bin" >> "$GITHUB_PATH"
export PATH="$CARGO_ROOT/bin:$PATH"

# Optional decoders improve coverage but must not block the core scanner.
OPTIONAL_PACKAGES=()
for package in jadx apktool rizin; do
  if apt-cache show "$package" >/dev/null 2>&1; then
    OPTIONAL_PACKAGES+=("$package")
  fi
done
if (("${#OPTIONAL_PACKAGES[@]}" > 0)); then
  sudo apt-get install -y "${OPTIONAL_PACKAGES[@]}"
fi

command -v jadx >/dev/null 2>&1 && jadx --version || echo "::warning::JADX unavailable; Androguard and direct APK scanning remain enabled."
command -v apktool >/dev/null 2>&1 && apktool --version || echo "::warning::Apktool unavailable; direct resource/archive scanning remains enabled."
command -v rizin >/dev/null 2>&1 && rizin -v || echo "::warning::Rizin unavailable; GNU strings/native ELF scanning remains enabled."

echo "Core acquisition tools installed."
java -version
"$APKEEP_BIN" --version
apksigner version
aapt version
