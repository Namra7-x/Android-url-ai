#!/usr/bin/env bash
# Install every tool ONCE, then cache the binaries in GitHub Actions.
# Hard-fail if anything is missing — no silent skips.
set -uo pipefail

export GOBIN="$HOME/go/bin"
export CARGOBIN="$HOME/.cargo/bin"
mkdir -p "$GOBIN" "$HOME/.local/bin" "$HOME/tools" "$HOME/.cache"
export PATH="$GOBIN:$CARGOBIN:$HOME/.local/bin:$PATH"

if [ -n "${GITHUB_PATH:-}" ]; then
  echo "$GOBIN" >> "$GITHUB_PATH"
  echo "$CARGOBIN" >> "$GITHUB_PATH"
  echo "$HOME/.local/bin" >> "$GITHUB_PATH"
fi

MARKER="$HOME/.cache/hunt-tools-ready"

REQUIRED="katana httpx ffuf uro subfinder dnsx uncover kr gau waybackurls jsluice urlfinder x8 jscope anastasis jq trufflehog gospider"

all_present() {
  for t in $REQUIRED; do
    command -v "$t" >/dev/null 2>&1 || return 1
  done
  [ -f "$HOME/tools/Anastasis/package.json" ] || return 1
  return 0
}

if [ -f "$MARKER" ] && all_present; then
  echo "Cached toolchain found — skipping all installs."
  exit 0
fi

# Native modules (tree-sitter for anastasis) need build tools BEFORE npm ci.
echo "::group::System tools"
sudo apt-get update -qq || true
sudo apt-get install -y -qq jq build-essential python3 >/dev/null 2>&1 || true
echo "::endgroup::"

echo "::group::Go tools"
go install github.com/projectdiscovery/katana/cmd/katana@latest || echo "WARN: katana"
go install github.com/projectdiscovery/httpx/cmd/httpx@latest || echo "WARN: httpx"
go install github.com/ffuf/ffuf/v2@latest || echo "WARN: ffuf"
go install github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest || echo "WARN: subfinder"
go install github.com/projectdiscovery/dnsx/cmd/dnsx@latest || echo "WARN: dnsx"
go install github.com/projectdiscovery/uncover/cmd/uncover@latest || echo "WARN: uncover"
go install github.com/assetnote/kiterunner/cmd/kiterunner@latest || echo "WARN: kiterunner"
if [ -x "$GOBIN/kiterunner" ] && [ ! -x "$GOBIN/kr" ]; then
  ln -s "$GOBIN/kiterunner" "$GOBIN/kr"
fi
go install github.com/lc/gau/v2/cmd/gau@latest || echo "WARN: gau"
go install github.com/tomnomnom/waybackurls@latest || echo "WARN: waybackurls"
go install github.com/jaeles-project/gospider@latest || echo "WARN: gospider"
go install github.com/BishopFox/jsluice/cmd/jsluice@latest || echo "WARN: jsluice"
# pinned to a Go-1.23-compatible release (verified on pkg.go.dev)
go install -v github.com/projectdiscovery/urlfinder/cmd/urlfinder@v0.0.3 || echo "WARN: urlfinder"
echo "::endgroup::"

echo "::group::Python tools"
python3 -m pip install --upgrade pip >/dev/null 2>&1 || true
# uro is Python (setup.py), jscope is a PyPI package (Python 3.10+)
python3 -m pip install uro jscope || echo "WARN: pip tools"
echo "::endgroup::"

echo "::group::Go release binaries (no compiler needed)"
# trufflehog official installer (verified working on the runner)
curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh \
  | sh -s -- -b "$GOBIN" || echo "WARN: trufflehog"
# x8 is Rust — prefer the official static Linux binary, no rustup needed
curl -sSfL https://github.com/Sh1Yo/x8/releases/download/v4.3.0/x86_64-linux-x8.gz \
  -o /tmp/x8.gz && gunzip -c /tmp/x8.gz > "$GOBIN/x8" && chmod +x "$GOBIN/x8" \
  || echo "WARN: x8 binary"
echo "::endgroup::"

echo "::group::Anastasis (Node 22 LTS, native modules)"
if [ ! -f "$HOME/tools/Anastasis/package.json" ]; then
  git clone --depth 1 https://github.com/0xazanul/Anastasis.git "$HOME/tools/Anastasis" || true
fi
if [ -d "$HOME/tools/Anastasis" ]; then
  cd "$HOME/tools/Anastasis"
  PUPPETEER_SKIP_DOWNLOAD=true npm ci --omit=optional >/dev/null 2>&1 || npm install --omit=optional >/dev/null 2>&1 || true
  npm run build >/dev/null 2>&1 || true
  # wrapper on PATH so hunt.py can call `anastasis`
  cat > "$HOME/.local/bin/anastasis" <<'EOF'
#!/usr/bin/env bash
cd "$HOME/tools/Anastasis" && exec npm run scan -- "$@"
EOF
  chmod +x "$HOME/.local/bin/anastasis"
fi
echo "::endgroup::"

echo "::group::Verify all tools"
MISSING=0
for t in $REQUIRED; do
  if command -v "$t" >/dev/null 2>&1; then
    echo "  OK   $t"
  else
    echo "  MISS $t"
    MISSING=1
  fi
done
echo "::endgroup::"

if [ "$MISSING" -ne 0 ]; then
  echo "::error::Required tools missing. No silent skips allowed."
  exit 1
fi
touch "$MARKER"
echo "All tools installed and cached."
