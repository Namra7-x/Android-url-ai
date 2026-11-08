#!/usr/bin/env bash
set -euo pipefail

TOOLS_DIR="\${RUNNER_TEMP:-/tmp}/android-url-atlas-tools"
mkdir -p "$TOOLS_DIR"
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update
sudo apt-get install -y curl jq unzip zip xz-utils p7zip-full file binutils

# GitHub release/CDN endpoints occasionally return transient 5xx responses.
# Retry downloads rather than failing the whole scan during a short outage.
retry_curl() {
  curl --fail --location --show-error \
    --retry 6 --retry-all-errors --retry-delay 5 \
    --connect-timeout 30 --max-time 1200 "$@"
}

asset_url() {
  local repo="$1" pattern="$2"
  retry_curl --silent "https://api.github.com/repos/$repo/releases/latest" \
    | jq -r --arg pattern "$pattern" \
      '.assets[] | select(.name | test($pattern)) | .browser_download_url' \
    | head -n 1
}

echo "Installing apkeep 1.1.0 (EFF release)..."
APKEEP_URL="https://github.com/EFForg/apkeep/releases/download/1.1.0/apkeep-x86_64-unknown-linux-gnu"
if retry_curl "$APKEEP_URL" -o "$TOOLS_DIR/apkeep"; then
  chmod +x "$TOOLS_DIR/apkeep"
else
  echo "::warning::apkeep release asset download failed; trying the pinned crates.io source build."
  sudo apt-get install -y cargo rustc pkg-config libssl-dev
  cargo install --locked --version 1.1.0 apkeep --root "$TOOLS_DIR/cargo" --force
  ln -sf "$TOOLS_DIR/cargo/bin/apkeep" "$TOOLS_DIR/apkeep"
fi
echo "$TOOLS_DIR" >> "$GITHUB_PATH"
export PATH="$TOOLS_DIR:$PATH"

# JADX, Apktool, Ghidra and Rizin improve coverage, but the APK archive scanner
# and Androguard must still run when one optional release server is unavailable.
JADX_URL="$(asset_url skylot/jadx '^jadx-[0-9].*\.zip$' || true)"
if [[ -n "$JADX_URL" ]] && retry_curl "$JADX_URL" -o "$TOOLS_DIR/jadx.zip"; then
  mkdir -p "$TOOLS_DIR/jadx"
  unzip -q "$TOOLS_DIR/jadx.zip" -d "$TOOLS_DIR/jadx"
  JADX_BIN="$(find "$TOOLS_DIR/jadx" -type f -path '*/bin/jadx' | head -n 1 || true)"
  if [[ -n "$JADX_BIN" ]]; then
    chmod +x "$JADX_BIN"
    echo "$(dirname "$JADX_BIN")" >> "$GITHUB_PATH"
    export PATH="$(dirname "$JADX_BIN"):$PATH"
  else
    echo "::warning::JADX archive contained no executable; continuing without JADX."
  fi
else
  echo "::warning::JADX download unavailable; APK archive and DEX passes remain enabled."
fi

APKTOOL_URL="$(asset_url iBotPeaches/Apktool '^apktool_[0-9].*\.jar$' || true)"
if [[ -n "$APKTOOL_URL" ]] && retry_curl "$APKTOOL_URL" -o "$TOOLS_DIR/apktool.jar"; then
  printf '#!/usr/bin/env bash\nexec java -jar "%s" "$@"\n' "$TOOLS_DIR/apktool.jar" > "$TOOLS_DIR/apktool"
  chmod +x "$TOOLS_DIR/apktool"
  echo "$TOOLS_DIR" >> "$GITHUB_PATH"
  export PATH="$TOOLS_DIR:$PATH"
else
  echo "::warning::Apktool download unavailable; continuing with JADX/Androguard/raw archive scanning."
fi

GHIDRA_URL="$(asset_url NationalSecurityAgency/ghidra '^ghidra_.*_PUBLIC_.*\.zip$' || true)"
if [[ -n "$GHIDRA_URL" ]] && retry_curl "$GHIDRA_URL" -o "$TOOLS_DIR/ghidra.zip"; then
  mkdir -p "$TOOLS_DIR/ghidra"
  unzip -q "$TOOLS_DIR/ghidra.zip" -d "$TOOLS_DIR/ghidra"
  GHIDRA_DIR="$(find "$TOOLS_DIR/ghidra" -maxdepth 1 -type d -name 'ghidra_*_PUBLIC' | head -n 1 || true)"
  if [[ -n "$GHIDRA_DIR" ]]; then
    echo "GHIDRA_HOME=$GHIDRA_DIR" >> "$GITHUB_ENV"
    echo "$GHIDRA_DIR/support" >> "$GITHUB_PATH"
    export PATH="$GHIDRA_DIR/support:$PATH"
  else
    echo "::warning::Ghidra archive could not be located; skipping native decompilation."
  fi
else
  echo "::warning::Ghidra download unavailable; ELF strings and Rizin passes remain enabled."
fi

RIZIN_URL="$(asset_url rizinorg/rizin '^rizin-v[0-9].*-static-x86_64\.tar\.xz$' || true)"
if [[ -n "$RIZIN_URL" ]] && retry_curl "$RIZIN_URL" -o "$TOOLS_DIR/rizin.tar.xz"; then
  mkdir -p "$TOOLS_DIR/rizin"
  tar -xJf "$TOOLS_DIR/rizin.tar.xz" -C "$TOOLS_DIR/rizin"
  RIZIN_BIN="$(find "$TOOLS_DIR/rizin" -type f -name rizin -perm -u+x | head -n 1 || true)"
  if [[ -n "$RIZIN_BIN" ]]; then
    echo "$(dirname "$RIZIN_BIN")" >> "$GITHUB_PATH"
    export PATH="$(dirname "$RIZIN_BIN"):$PATH"
  fi
else
  echo "::warning::Rizin release unavailable; strings and Ghidra passes continue."
fi

echo "Tool installation completed."
java -version
"$TOOLS_DIR/apkeep" --version || "$TOOLS_DIR/apkeep" --help >/dev/null
command -v jadx >/dev/null 2>&1 && jadx --version || true
command -v apktool >/dev/null 2>&1 && apktool --version || true
apksigner version
aapt version
