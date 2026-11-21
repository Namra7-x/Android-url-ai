#!/usr/bin/env bash
# Install every tool the hunt pipeline needs.
# FAIL LOUDLY if anything is missing — no silent skips, ever.
set -uo pipefail

export GOBIN="$HOME/go/bin"
mkdir -p "$GOBIN" "$HOME/.local/bin" "$HOME/tools"
export PATH="$GOBIN:$HOME/.local/bin:$PATH"

if [ -n "${GITHUB_PATH:-}" ]; then
  echo "$GOBIN" >> "$GITHUB_PATH"
  echo "$HOME/.local/bin" >> "$GITHUB_PATH"
fi

echo "::group::Go tools"
go install github.com/projectdiscovery/katana/cmd/katana@latest || echo "WARN: katana"
go install github.com/projectdiscovery/httpx/cmd/httpx@latest || echo "WARN: httpx"
go install github.com/ffuf/ffuf/v2@latest || echo "WARN: ffuf"
go install github.com/s0md3v/uro@latest || echo "WARN: uro"
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest || echo "WARN: subfinder"
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest || echo "WARN: dnsx"
go install github.com/projectdiscovery/uncover/cmd/uncover@latest || echo "WARN: uncover"
go install github.com/assetnote/kiterunner/cmd/kr@latest || echo "WARN: kiterunner"
go install github.com/lc/gau/v2/cmd/gau@latest || echo "WARN: gau"
go install github.com/tomnomnom/waybackurls@latest || echo "WARN: waybackurls"
go install github.com/BishopFox/jsluice/cmd/jsluice@latest || echo "WARN: jsluice"
echo "::endgroup::"

echo "::group::TruffleHog (official prebuilt binary — no Go build needed)"
curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh \
  | sh -s -- -b "$GOBIN" || echo "WARN: trufflehog"
echo "::endgroup::"

echo "::group::Python tools"
python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
# xnLinkFinder now installs as a CLI on PATH (v8.2) — no clone/path guessing.
python3 -m pip install waymore arjun xnLinkFinder || echo "WARN: pip tools"
echo "::endgroup::"

echo "::group::Chakra"
git clone --depth 1 https://github.com/NavyTitanium/Chakra.git "$HOME/tools/Chakra" || true
python3 -m pip install requests jsbeautifier brotlicffi || echo "WARN: chakra python deps"
echo "::endgroup::"

echo "::group::Node tools"
npm install -g @js-recon/js-recon || echo "WARN: js-recon"
npx --yes puppeteer browsers install chrome || true
echo "::endgroup::"

echo "::group::System tools"
sudo apt-get update -qq || true
sudo apt-get install -y -qq jq >/dev/null 2>&1 || true
echo "::endgroup::"

# ---------------------------------------------------------------------------
# HARD VERIFICATION — a missing tool fails the job here, not silently later.
# ---------------------------------------------------------------------------
echo "::group::Verify all tools"
REQUIRED="katana httpx ffuf uro subfinder dnsx uncover kr gau waybackurls jsluice trufflehog waymore arjun js-recon jq xnLinkFinder"
MISSING=0
for t in $REQUIRED; do
  if command -v "$t" >/dev/null 2>&1; then
    echo "  OK   $t"
  else
    echo "  MISS $t"
    MISSING=1
  fi
done
if [ -f "$HOME/tools/Chakra/chakra.py" ]; then
  echo "  OK   Chakra"
else
  echo "  MISS Chakra"
  MISSING=1
fi
echo "::endgroup::"

if [ "$MISSING" -ne 0 ]; then
  echo "::error::One or more required tools are missing. No silent skips allowed."
  exit 1
fi
echo "All tools installed and verified."
