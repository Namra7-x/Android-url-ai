#!/usr/bin/env python3
"""
Public artifact probe utility.

Read-only, anonymous probing of public endpoints only. This tool is intentionally
conservative:

- It verifies TLS certificates.
- It refuses credential-bearing headers (Authorization, Cookie, API-key headers).
- It labels model-like matches as candidates, never as confirmed leaks.
- It stops at 401/403/405 and reports the surface as blocked.

Usage:
    python probe_endpoint.py <url> [--method GET|POST] [--body <json_str>]
                             [--header "Origin: https://example.com"]
                             [--filter <regex>] [--timeout 15]
                             [--max-bytes 200000]
"""

import argparse
import gzip
import json
import re
import ssl
import time
import urllib.error
import urllib.request

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/131.0.0.0 Safari/537.36"
)

# Broad, context-free candidate patterns. These are leads, not findings.
CANDIDATE_REGEX = re.compile(
    r"(?:gpt|claude|gemini|grok|qwen|deepseek|mistral|llama|imagen|veo|lyria)"
    r"[-_a-z0-9.]{2,}",
    re.IGNORECASE,
)

# Redact common credential shapes if they ever appear in a printed match.
SECRET_REGEX = re.compile(
    r"(?:AIza[0-9A-Za-z_-]{20,}|sk-[A-Za-z0-9]{20,}|"
    r"gh[pousr]_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,})"
)

BLOCKED_STATUS = {401, 403, 405}
BLOCKED_HEADERS = {
    "authorization",
    "cookie",
    "set-cookie",
    "x-goog-api-key",
    "x-api-key",
    "proxy-authorization",
}


def redact(value):
    return SECRET_REGEX.sub("[REDACTED]", value)


def parse_headers(raw_headers):
    headers = {}
    for raw in raw_headers:
        if ":" not in raw:
            raise SystemExit(f"Invalid header (expected 'Name: value'): {raw}")
        name, value = raw.split(":", 1)
        name = name.strip()
        if name.lower() in BLOCKED_HEADERS:
            raise SystemExit(
                f"Refusing credential-bearing header '{name}'. "
                "This tool is for anonymous public artifacts only."
            )
        headers[name] = value.strip()
    return headers


def probe(
    url,
    method="GET",
    body=None,
    headers=None,
    timeout=15,
    max_bytes=200000,
    filter_pattern=None,
):
    start = time.time()
    req_headers = {"User-Agent": DEFAULT_UA, "Accept": "*/*"}
    if headers:
        req_headers.update(headers)

    data = body.encode("utf-8") if body else None
    req = urllib.request.Request(url, data=data, headers=req_headers, method=method)

    print(f"[*] Probing {method} {url}")
    try:
        context = ssl.create_default_context()
        with urllib.request.urlopen(req, context=context, timeout=timeout) as resp:
            status = resp.status
            content_type = resp.headers.get("Content-Type", "")
            content_length = resp.headers.get("Content-Length", "unknown")
            cache_hint = resp.headers.get(
                "Last-Modified", resp.headers.get("ETag", "none")
            )
            raw = resp.read(max_bytes)

            if resp.headers.get("Content-Encoding") == "gzip":
                try:
                    raw = gzip.decompress(raw)
                except Exception:
                    pass

            elapsed = round(time.time() - start, 2)
            print(
                f"[+] HTTP {status} in {elapsed}s | "
                f"Type: {content_type} | Length: {content_length} | "
                f"Last-Mod/ETag: {cache_hint}"
            )

            text = raw.decode("utf-8", errors="ignore")

            # Strip common anti-hijack prefixes before JSON parsing.
            for prefix in (")]}'", "while(1);", "for(;;);"):
                if text.startswith(prefix):
                    print(f"[*] Stripped anti-hijack prefix: {prefix!r}")
                    text = text[len(prefix):].lstrip()
                    break

            try:
                parsed = json.loads(text)
                if isinstance(parsed, list):
                    print(f"[+] JSON array, {len(parsed)} item(s) in sampled chunk.")
                    if parsed and isinstance(parsed[0], dict):
                        print(f"    Sample keys: {list(parsed[0].keys())[:8]}")
                elif isinstance(parsed, dict):
                    print(f"[+] JSON object, keys: {list(parsed.keys())[:10]}")
                    for key in ("models", "items", "skus", "summaries", "products"):
                        value = parsed.get(key)
                        if isinstance(value, list):
                            print(f"    Key '{key}' contains {len(value)} entries.")
                        elif isinstance(value, dict):
                            print(f"    Key '{key}' contains {len(value)} entries.")
            except Exception:
                print("[-] Non-JSON response or partial stream.")

            candidates = sorted(set(CANDIDATE_REGEX.findall(text)))
            if candidates:
                sample = ", ".join(redact(x) for x in candidates[:12])
                print(
                    f"[*] Candidate identifier patterns (not a leak): "
                    f"{len(candidates)} match(es): {sample}"
                )
            else:
                print("[*] No candidate model-like patterns in sampled chunk.")

            if filter_pattern:
                try:
                    regex = re.compile(filter_pattern)
                    matches = sorted({str(m) for m in regex.findall(text)})
                    if matches:
                        sample = ", ".join(redact(x) for x in matches[:20])
                        print(
                            f"[*] Filter matches (not a leak): "
                            f"{len(matches)} match(es): {sample}"
                        )
                    else:
                        print("[*] Filter matched nothing in sampled chunk.")
                except re.error as exc:
                    print(f"[-] Invalid filter regex: {exc}")

    except urllib.error.HTTPError as exc:
        if exc.code in BLOCKED_STATUS:
            print(f"[!] Blocked (HTTP {exc.code}) — surface exists, not a leak.")
        else:
            print(f"[-] HTTP error {exc.code}: {exc.reason}")
    except urllib.error.URLError as exc:
        print(f"[-] Request failed: {exc.reason}")
    except Exception as exc:
        print(f"[-] Request failed: {exc}")


def main():
    parser = argparse.ArgumentParser(
        description="Probe a public endpoint for anonymous, read-only evidence."
    )
    parser.add_argument("url", help="Public URL to probe")
    parser.add_argument(
        "--method", default="GET", choices=["GET", "POST"], help="HTTP method"
    )
    parser.add_argument("--body", default=None, help="JSON body for POST")
    parser.add_argument(
        "--header",
        action="append",
        default=[],
        help="Extra header, e.g. 'Origin: https://example.com'",
    )
    parser.add_argument("--filter", default=None, help="Optional regex to sample")
    parser.add_argument("--timeout", type=int, default=15, help="Timeout in seconds")
    parser.add_argument(
        "--max-bytes", type=int, default=200000, help="Maximum bytes to read"
    )
    args = parser.parse_args()

    custom_headers = parse_headers(args.header)
    if args.body:
        custom_headers.setdefault("Content-Type", "application/json")

    probe(
        args.url,
        method=args.method,
        body=args.body,
        headers=custom_headers,
        timeout=args.timeout,
        max_bytes=args.max_bytes,
        filter_pattern=args.filter,
    )


if __name__ == "__main__":
    main()
