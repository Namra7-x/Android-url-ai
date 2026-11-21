#!/usr/bin/env bash
# Install all CLI tools on an Ubuntu GitHub runner.
# Failures are logged but do not stop the job (optional tools may be unavailable).
set -uo pipefail

export GOBIN="$HOME/go/bin"
mkdir -p "$GOBIN"
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
go install github.com/trufflesecurity/trufflehog/v3@latest || echo "WARN: trufflehog"
echo "::endgroup::"

echo "::group::Python tools"
python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
python3 -m pip install waymore arjun || echo "WARN: pip waymore/arjun"

mkdir -p "$HOME/tools"
git clone --depth 1 https://github.com/NavyTitanium/Chakra.git "$HOME/tools/Chakra" || true
python3 -m pip install requests jsbeautifier brotlicffi || true

git clone --depth 1 https://github.com/xnl-h4ck3r/xnLinkFinder.git "$HOME/tools/xnLinkFinder" || true
if [ -f "$HOME/tools/xnLinkFinder/requirements.txt" ]; then
  python3 -m pip install -r "$HOME/tools/xnLinkFinder/requirements.txt" || true
fi
echo "::endgroup::"

echo "::group::Node tools"
npm install -g @js-recon/js-recon || echo "WARN: js-recon"
npx --yes puppeteer browsers install chrome || true
echo "::endgroup::"

echo "::group::System tools"
sudo apt-get update -qq || true
sudo apt-get install -y -qq jq >/dev/null 2>&1 || true
echo "::endgroup::"

echo "Installed versions:"
for t in katana httpx ffuf uro subfinder dnsx uncover kr gau waybackurls jsluice trufflehog waymore arjun js-recon jq; do
  if command -v "$t" >/dev/null 2>&1; then
    echo "  OK  $t"
  else
    echo "  --  $t (missing)"
  fi
done
