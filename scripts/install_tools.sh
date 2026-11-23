#!/usr/bin/env bash
# Install ONLY what is missing. Everything lands in cached paths, so repeat
# runs (and runs after installer edits, via restore-keys) do ZERO installs.
set -uo pipefail

export GOBIN="$HOME/go/bin"
export TOOLS_BIN="$HOME/tools/bin"
mkdir -p "$GOBIN" "$TOOLS_BIN" "$HOME/.local/bin" "$HOME/tools" "$HOME/.cache"
export PATH="$GOBIN:$TOOLS_BIN:$HOME/.local/bin:$PATH"

if [ -n "${GITHUB_PATH:-}" ]; then
  {
    echo "$GOBIN"
    echo "$TOOLS_BIN"
    echo "$HOME/.local/bin"
  } >> "$GITHUB_PATH"
fi

MARKER="$HOME/.cache/hunt-tools-ready"
have() { command -v "$1" >/dev/null 2>&1; }

REQUIRED="katana httpx ffuf uro subfinder dnsx uncover kr waybackurls jsluice urlfinder x8 jscope anastasis jq trufflehog cariddi noseyparker getJS subjs nuclei"

all_present() {
  for t in $REQUIRED; do have "$t" || return 1; done
  [ -f "$HOME/tools/Anastasis/package.json" ] || return 1
  return 0
}

if [ -f "$MARKER" ] && all_present; then
  echo "Cached toolchain complete — ZERO installs this run."
  exit 0
fi

echo "::group::System deps"
if ! have jq || ! have unzip; then
  sudo apt-get update -qq || true
  sudo apt-get install -y -qq jq unzip build-essential python3 >/dev/null 2>&1 || true
fi
echo "::endgroup::"

echo "::group::Go tools (only missing ones)"
have katana     || go install github.com/projectdiscovery/katana/cmd/katana@latest || echo "WARN katana"
have httpx      || go install github.com/projectdiscovery/httpx/cmd/httpx@latest || echo "WARN httpx"
have ffuf       || go install github.com/ffuf/ffuf/v2@latest || echo "WARN ffuf"
have subfinder  || go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest || echo "WARN subfinder"
have dnsx       || go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest || echo "WARN dnsx"
have uncover    || go install github.com/projectdiscovery/uncover/cmd/uncover@latest || echo "WARN uncover"
if ! have kr; then
  go install github.com/assetnote/kiterunner/cmd/kiterunner@latest || echo "WARN kiterunner"
  [ -x "$GOBIN/kiterunner" ] && ln -sf "$GOBIN/kiterunner" "$GOBIN/kr"
fi
have waybackurls || go install github.com/tomnomnom/waybackurls@latest || echo "WARN waybackurls"
have jsluice    || go install github.com/BishopFox/jsluice/cmd/jsluice@latest || echo "WARN jsluice"
# dev branch carries the source fixes (#139/#136/#154) missing from v0.0.3
have urlfinder  || go install -v github.com/projectdiscovery/urlfinder/cmd/urlfinder@dev || echo "WARN urlfinder"
have getJS      || go install github.com/003random/getJS@latest || echo "WARN getJS"
have subjs      || go install github.com/lc/subjs@latest || echo "WARN subjs"
have nuclei     || go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest || echo "WARN nuclei"
echo "::endgroup::"

echo "::group::Python tools (user site = cached)"
have uro    || python3 -m pip install --user uro || echo "WARN uro"
have jscope || python3 -m pip install --user jscope || echo "WARN jscope"
echo "::endgroup::"

echo "::group::Prebuilt binaries (no compiler)"
if ! have trufflehog; then
  curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh \
    | sh -s -- -b "$GOBIN" || echo "WARN trufflehog"
fi
if ! have x8; then
  curl -sSfL https://github.com/Sh1Yo/x8/releases/download/v4.3.0/x86_64-linux-x8.gz -o /tmp/x8.gz \
    && gunzip -c /tmp/x8.gz > "$TOOLS_BIN/x8" && chmod +x "$TOOLS_BIN/x8" || echo "WARN x8"
fi
if ! have cariddi; then
  curl -sSfL https://github.com/edoardottt/cariddi/releases/download/v1.4.6/cariddi_1.4.6_linux_amd64.zip -o /tmp/cariddi.zip \
    && unzip -o -q /tmp/cariddi.zip -d /tmp/cariddi \
    && find /tmp/cariddi -type f -name cariddi -exec mv {} "$TOOLS_BIN/cariddi" \; \
    && chmod +x "$TOOLS_BIN/cariddi" || echo "WARN cariddi"
fi
if ! have noseyparker; then
  curl -sSfL https://github.com/praetorian-inc/noseyparker/releases/download/v0.24.0/noseyparker-v0.24.0-x86_64-unknown-linux-musl.tar.gz -o /tmp/np.tgz \
    && mkdir -p /tmp/np && tar -xzf /tmp/np.tgz -C /tmp/np \
    && find /tmp/np -type f -name noseyparker -exec mv {} "$TOOLS_BIN/noseyparker" \; \
    && chmod +x "$TOOLS_BIN/noseyparker" || echo "WARN noseyparker"
fi
echo "::endgroup::"

echo "::group::Anastasis (cached whole folder)"
if [ ! -f "$HOME/tools/Anastasis/package.json" ]; then
  git clone --depth 1 https://github.com/0xazanul/Anastasis.git "$HOME/tools/Anastasis" || true
fi
if [ -d "$HOME/tools/Anastasis" ] && [ ! -d "$HOME/tools/Anastasis/dist" ]; then
  ( cd "$HOME/tools/Anastasis" \
    && PUPPETEER_SKIP_DOWNLOAD=true npm ci >/dev/null 2>&1 || npm install >/dev/null 2>&1 || true )
  ( cd "$HOME/tools/Anastasis" && npm run build >/dev/null 2>&1 || true )
fi
if [ -d "$HOME/tools/Anastasis" ] && ! have anastasis; then
  cat > "$HOME/.local/bin/anastasis" <<'EOF'
#!/usr/bin/env bash
cd "$HOME/tools/Anastasis" && exec npm run scan -- "$@"
EOF
  chmod +x "$HOME/.local/bin/anastasis"
fi
echo "::endgroup::"

echo "::group::Chrome + nuclei templates (cached)"
if [ ! -d "$HOME/.cache/puppeteer" ] || [ -z "$(ls -A "$HOME/.cache/puppeteer" 2>/dev/null)" ]; then
  npx --yes puppeteer browsers install chrome >/dev/null 2>&1 || true
fi
if have nuclei && [ ! -d "$HOME/nuclei-templates" ]; then
  nuclei -update-templates -silent >/dev/null 2>&1 || true
fi
echo "::endgroup::"

echo "::group::Verify"
MISSING=0
for t in $REQUIRED; do
  if have "$t"; then echo "  OK   $t"; else echo "  MISS $t"; MISSING=1; fi
done
echo "::endgroup::"
if [ "$MISSING" -ne 0 ]; then
  echo "::error::Required tools missing."
  exit 1
fi
touch "$MARKER"
echo "Toolchain ready (cached for next runs)."
