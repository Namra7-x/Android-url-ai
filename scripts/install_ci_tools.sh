#!/usr/bin/env bash
set -euo pipefail
TOOLS_DIR="\${RUNNER_TEMP:-/tmp}/android-url-atlas-tools"
mkdir -p "$TOOLS_DIR"
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update
sudo apt-get install -y curl jq unzip zip xz-utils p7zip-full file binutils

asset_url() {
  local repo="$1" pattern="$2"
  curl -fsSL "https://api.github.com/repos/$repo/releases/latest" \
    | jq -r --arg pattern "$pattern" '.assets[] | select(.name | test($pattern)) | .browser_download_url' \
    | head -n 1
}

SDK_ROOT="$TOOLS_DIR/android-sdk"
mkdir -p "$SDK_ROOT/cmdline-tools"
curl -fL "https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip" -o "$TOOLS_DIR/android-cmdline-tools.zip"
mkdir -p "$SDK_ROOT/cmdline-tools/latest"
unzip -q "$TOOLS_DIR/android-cmdline-tools.zip" -d "$SDK_ROOT/cmdline-tools"
if [[ -d "$SDK_ROOT/cmdline-tools/cmdline-tools" ]]; then
  mv "$SDK_ROOT/cmdline-tools/cmdline-tools/"* "$SDK_ROOT/cmdline-tools/latest/"
  rmdir "$SDK_ROOT/cmdline-tools/cmdline-tools"
fi
export ANDROID_HOME="$SDK_ROOT"
export ANDROID_SDK_ROOT="$SDK_ROOT"
export PATH="$SDK_ROOT/cmdline-tools/latest/bin:$PATH"
yes | sdkmanager --licenses >/dev/null
sdkmanager "platform-tools" "build-tools;35.0.0" >/dev/null
echo "$SDK_ROOT/platform-tools" >> "$GITHUB_PATH"
echo "$SDK_ROOT/build-tools/35.0.0" >> "$GITHUB_PATH"
echo "ANDROID_HOME=$SDK_ROOT" >> "$GITHUB_ENV"
echo "ANDROID_SDK_ROOT=$SDK_ROOT" >> "$GITHUB_ENV"

JADX_URL="$(asset_url skylot/jadx '^jadx-[0-9].*\.zip$')"
test -n "$JADX_URL"
curl -fL "$JADX_URL" -o "$TOOLS_DIR/jadx.zip"
mkdir -p "$TOOLS_DIR/jadx"
unzip -q "$TOOLS_DIR/jadx.zip" -d "$TOOLS_DIR/jadx"
JADX_BIN="$(find "$TOOLS_DIR/jadx" -type f -path '*/bin/jadx' | head -n 1)"
test -n "$JADX_BIN"
chmod +x "$JADX_BIN"
echo "$(dirname "$JADX_BIN")" >> "$GITHUB_PATH"

APKTOOL_URL="$(asset_url iBotPeaches/Apktool '^apktool_[0-9].*\.jar$')"
test -n "$APKTOOL_URL"
curl -fL "$APKTOOL_URL" -o "$TOOLS_DIR/apktool.jar"
printf '#!/usr/bin/env bash\nexec java -jar "%s" "$@"\n' "$TOOLS_DIR/apktool.jar" > "$TOOLS_DIR/apktool"
chmod +x "$TOOLS_DIR/apktool"
echo "$TOOLS_DIR" >> "$GITHUB_PATH"

GHIDRA_URL="$(asset_url NationalSecurityAgency/ghidra '^ghidra_.*_PUBLIC_.*\.zip$')"
test -n "$GHIDRA_URL"
curl -fL "$GHIDRA_URL" -o "$TOOLS_DIR/ghidra.zip"
mkdir -p "$TOOLS_DIR/ghidra"
unzip -q "$TOOLS_DIR/ghidra.zip" -d "$TOOLS_DIR/ghidra"
GHIDRA_DIR="$(find "$TOOLS_DIR/ghidra" -maxdepth 1 -type d -name 'ghidra_*_PUBLIC' | head -n 1)"
test -n "$GHIDRA_DIR"
echo "GHIDRA_HOME=$GHIDRA_DIR" >> "$GITHUB_ENV"
echo "$GHIDRA_DIR/support" >> "$GITHUB_PATH"

RIZIN_URL="$(asset_url rizinorg/rizin '^rizin-v[0-9].*-static-x86_64\.tar\.xz$')"
if [[ -n "$RIZIN_URL" ]]; then
  curl -fL "$RIZIN_URL" -o "$TOOLS_DIR/rizin.tar.xz"
  mkdir -p "$TOOLS_DIR/rizin"
  tar -xJf "$TOOLS_DIR/rizin.tar.xz" -C "$TOOLS_DIR/rizin"
  RIZIN_BIN="$(find "$TOOLS_DIR/rizin" -type f -name rizin -perm -u+x | head -n 1 || true)"
  if [[ -n "$RIZIN_BIN" ]]; then echo "$(dirname "$RIZIN_BIN")" >> "$GITHUB_PATH"; fi
else
  echo "::warning::Rizin release unavailable; strings and Ghidra passes continue."
fi

echo "Tool installation completed."
java -version
jadx --version
apktool --version
apksigner version
aapt version
analyzeHeadless -help >/dev/null
