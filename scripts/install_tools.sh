#!/usr/bin/env bash
# Install ONLY missing runtime tools into cached paths (~/.local, ~/go/bin, ~/tools/bin).
# When the runtime cache hits, this exits in <1s without touching Go/Node/pip.
set -uo pipefail

export GOBIN="$HOME/go/bin"
export TOOLS_BIN="$HOME/tools/bin"
export PYTHONUSERBASE="$HOME/.local"
mkdir -p "$GOBIN" "$TOOLS_BIN" "$HOME/.local/bin" "$HOME/tools" "$HOME/.cache" "$HOME/.cache/chrome-headless-shell"
export PATH="$GOBIN:$TOOLS_BIN:$HOME/.local/bin:$PATH"

if [ -n "${GITHUB_PATH:-}" ]; then
  {
    echo "$GOBIN"
    echo "$TOOLS_BIN"
    echo "$HOME/.local/bin"
  } >> "$GITHUB_PATH"
fi

MARKER="$HOME/.cache/hunt-tools-ready-v3"
have() { command -v "$1" >/dev/null 2>&1; }

REQUIRED="katana httpx ffuf uro subfinder dnsx uncover jsluice urlfinder x8 jscope waymore xnLinkFinder jq trufflehog titus feroxbuster sourcemapper nuclei"

has_scrapling() {
  python3 -c "import scrapling" >/dev/null 2>&1
}

has_headless_shell() {
  have chrome-headless-shell || [ -n "$(find "$HOME/.cache/chrome-headless-shell" -type f -name "chrome-headless-shell" 2>/dev/null | head -n 1)" ]
}

link_headless_shell() {
  local bin
  bin=$(find "$HOME/.cache/chrome-headless-shell" -type f -name "chrome-headless-shell" 2>/dev/null | head -n 1 || true)
  if [ -n "$bin" ] && [ -x "$bin" ]; then
    ln -sf "$bin" "$TOOLS_BIN/chrome-headless-shell"
  fi
}

all_present() {
  for t in $REQUIRED; do
    have "$t" || return 1
  done
  has_scrapling || return 1
  has_headless_shell || return 1
  [ -d "$HOME/nuclei-templates" ] || return 1
  return 0
}

link_headless_shell

if [ -f "$MARKER" ] && all_present; then
  echo "Cached toolchain v3 complete — ZERO installs this run."
  exit 0
fi

echo "::group::System deps"
if ! have jq || ! have unzip || ! have curl; then
  sudo apt-get update -qq || true
  sudo apt-get install -y -qq jq unzip curl ca-certificates python3 >/dev/null 2>&1 || true
fi
echo "::endgroup::"

echo "::group::Go tools (only missing ones)"
if have go; then
  have katana       || go install github.com/projectdiscovery/katana/cmd/katana@latest || echo "WARN katana"
  have httpx        || go install github.com/projectdiscovery/httpx/cmd/httpx@latest || echo "WARN httpx"
  have ffuf         || go install github.com/ffuf/ffuf/v2@latest || echo "WARN ffuf"
  have subfinder    || go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest || echo "WARN subfinder"
  have dnsx         || go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest || echo "WARN dnsx"
  have uncover      || go install github.com/projectdiscovery/uncover/cmd/uncover@latest || echo "WARN uncover"
  have jsluice      || go install github.com/BishopFox/jsluice/cmd/jsluice@latest || echo "WARN jsluice"
  have urlfinder    || go install -v github.com/projectdiscovery/urlfinder/cmd/urlfinder@dev || echo "WARN urlfinder"
  have sourcemapper || go install github.com/denandz/sourcemapper@latest || echo "WARN sourcemapper"
  have nuclei       || go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest || echo "WARN nuclei"
else
  echo "WARN go not installed; skipping Go installs"
fi
echo "::endgroup::"

echo "::group::Python tools (user site = cached)"
python3 -m pip install --user --upgrade pip >/dev/null 2>&1 || true
have uro          || python3 -m pip install --user uro || echo "WARN uro"
have jscope       || python3 -m pip install --user jscope || echo "WARN jscope"
have waymore      || python3 -m pip install --user waymore || echo "WARN waymore"
if ! have xnLinkFinder; then
  python3 -m pip install --user xnLinkFinder || python3 -m pip install --user git+https://github.com/xnl-h4ck3r/xnLinkFinder.git || echo "WARN xnLinkFinder"
  if ! have xnLinkFinder && have xnlinkfinder; then
    ln -sf "$(command -v xnlinkfinder)" "$HOME/.local/bin/xnLinkFinder"
  fi
fi
if ! has_scrapling; then
  python3 -m pip install --user "scrapling[all]" || python3 -m pip install --user "scrapling[fetchers]" || echo "WARN scrapling"
fi
if has_scrapling && { [ ! -d "$HOME/.cache/ms-playwright" ] || [ -z "$(ls -A "$HOME/.cache/ms-playwright" 2>/dev/null)" ]; }; then
  scrapling install || python3 -m scrapling install || echo "WARN scrapling install"
fi
echo "::endgroup::"

echo "::group::Prebuilt binaries (no compiler)"
if ! have trufflehog; then
  curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh \
    | sh -s -- -b "$TOOLS_BIN" || echo "WARN trufflehog"
fi

if ! have x8; then
  curl -sSfL https://github.com/Sh1Yo/x8/releases/download/v4.3.0/x86_64-linux-x8.gz -o /tmp/x8.gz \
    && gunzip -c /tmp/x8.gz > "$TOOLS_BIN/x8" && chmod +x "$TOOLS_BIN/x8" || echo "WARN x8"
fi

if ! have feroxbuster; then
  if curl -sSfL https://github.com/epi052/feroxbuster/releases/latest/download/x86_64-linux-feroxbuster.tar.gz -o /tmp/ferox.tar.gz 2>/dev/null; then
    mkdir -p /tmp/ferox && tar -xzf /tmp/ferox.tar.gz -C /tmp/ferox \
      && find /tmp/ferox -type f -name feroxbuster -exec mv {} "$TOOLS_BIN/feroxbuster" \; \
      && chmod +x "$TOOLS_BIN/feroxbuster"
  elif curl -sSfL https://github.com/epi052/feroxbuster/releases/latest/download/x86_64-linux-feroxbuster.zip -o /tmp/ferox.zip 2>/dev/null; then
    mkdir -p /tmp/ferox && unzip -o -q /tmp/ferox.zip -d /tmp/ferox \
      && find /tmp/ferox -type f -name feroxbuster -exec mv {} "$TOOLS_BIN/feroxbuster" \; \
      && chmod +x "$TOOLS_BIN/feroxbuster"
  else
    echo "WARN feroxbuster"
  fi
fi

if ! have titus; then
  TITUS_URL=$(curl -sSfL https://api.github.com/repos/praetorian-inc/titus/releases/latest 2>/dev/null \
    | jq -r '.assets[]?.browser_download_url | select(test("linux.*(amd64|x86_64)"; "i"))' | head -n 1 || true)
  if [ -z "$TITUS_URL" ]; then
    TITUS_URL="https://github.com/praetorian-inc/titus/releases/latest/download/titus-linux-amd64"
  fi
  if curl -sSfL "$TITUS_URL" -o /tmp/titus_dl; then
    case "$TITUS_URL" in
      *.tar.gz|*.tgz)
        mkdir -p /tmp/titus_ext && tar -xzf /tmp/titus_dl -C /tmp/titus_ext \
          && find /tmp/titus_ext -type f -name "titus*" -exec mv {} "$TOOLS_BIN/titus" \;
        ;;
      *.zip)
        mkdir -p /tmp/titus_ext && unzip -o -q /tmp/titus_dl -d /tmp/titus_ext \
          && find /tmp/titus_ext -type f -name "titus*" -exec mv {} "$TOOLS_BIN/titus" \;
        ;;
      *)
        mv /tmp/titus_dl "$TOOLS_BIN/titus"
        ;;
    esac
    chmod +x "$TOOLS_BIN/titus" 2>/dev/null || true
  else
    echo "WARN titus"
  fi
fi
echo "::endgroup::"

echo "::group::chrome-headless-shell + nuclei templates (cached)"
if ! has_headless_shell; then
  if have npx; then
    npx --yes @puppeteer/browsers install chrome-headless-shell@stable --path "$HOME/.cache/chrome-headless-shell" >/dev/null 2>&1 || echo "WARN chrome-headless-shell"
    link_headless_shell
  else
    echo "WARN npx missing; skipping chrome-headless-shell"
  fi
fi

if have nuclei && [ ! -d "$HOME/nuclei-templates" ]; then
  nuclei -update-templates -silent >/dev/null 2>&1 || echo "WARN nuclei-templates"
fi
echo "::endgroup::"

echo "::group::Verify toolchain"
MISSING=0
for t in $REQUIRED; do
  if have "$t"; then
    echo "  OK   $t"
  else
    echo "  MISS $t"
    MISSING=1
  fi
done
if has_scrapling; then echo "  OK   scrapling"; else echo "  MISS scrapling"; MISSING=1; fi
if has_headless_shell; then echo "  OK   chrome-headless-shell"; else echo "  MISS chrome-headless-shell"; fi
if [ -d "$HOME/nuclei-templates" ]; then echo "  OK   nuclei-templates"; else echo "  MISS nuclei-templates"; fi
echo "::endgroup::"

if [ "$MISSING" -ne 0 ]; then
  echo "::error::Required tools missing."
  exit 1
fi

touch "$MARKER"
echo "Toolchain v3 ready (cached for future runs)."
