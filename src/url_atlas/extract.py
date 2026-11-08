from __future__ import annotations
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

URL_RE = re.compile(rb"(?i)(?:https?|wss?|ftp)://[^\s\x00\"'<>\\{}\[\]]{3,2048}")
DOMAIN_RE = re.compile(rb"(?i)(?<![a-z0-9_-])(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+(?:com|net|org|io|ai|app|dev|co|uk|in|us|edu|gov|cloud|google|googleapis|gstatic|me|xyz|tech|info|biz|tv|gg|so)(?:/[^\s\x00\"'<>\\{}\[\]]{0,1024})?")
CUSTOM_RE = re.compile(rb"(?i)\b(?:[a-z][a-z0-9+.-]{1,30})://[^\s\x00\"'<>\\{}\[\]]{1,1024}")
SECRET_KEYS = {"token","access_token","refresh_token","id_token","api_key","apikey","key","authorization","auth","signature","sig","password","code","session","sessionid"}

def candidates(data: bytes):
    for pattern, label in ((URL_RE,"bytes-ascii"),(DOMAIN_RE,"bytes-domain"),(CUSTOM_RE,"bytes-custom-uri")):
        for match in pattern.finditer(data):
            yield match.group(0).decode("utf-8","replace"), label
    # Scan UTF-16LE literals too (common in native code and resources).
    text = data.decode("utf-16le","ignore")
    if text:
        encoded = text.encode("utf-8","ignore")
        for pattern in (URL_RE, DOMAIN_RE):
            for match in pattern.finditer(encoded):
                yield match.group(0).decode("utf-8","replace"), "utf16le"

def redact_url(value: str) -> str:
    value = value.strip().rstrip(".,;:!?)]}")
    try:
        p = urlsplit(value)
        if not p.scheme:
            return value
        query = []
        for item in p.query.split("&") if p.query else []:
            k, sep, v = item.partition("=")
            if k.lower() in SECRET_KEYS and sep:
                v = "[REDACTED]"
            query.append(k + (("=" + v) if sep else ""))
        return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path, "&".join(query), ""))
    except ValueError:
        return value

def classify_url(url: str) -> str:
    low = url.lower()
    if low.startswith(("ws://","wss://")):
        return "websocket"
    if not low.startswith(("http://","https://")):
        return "custom-uri"
    path = urlsplit(url).path.lower()
    if any(x in path for x in ("/graphql","/api/","/v1/","/v2/","/rpc","/rest/")):
        return "api"
    if any(x in urlsplit(url).netloc.lower() for x in ("cdn","static","assets","gstatic")):
        return "asset-or-cdn"
    return "http-url"

def scan_file(path: Path, root: Path, app: str, version: str, method="raw-byte-scan"):
    try:
        data = path.read_bytes()
    except OSError:
        return []
    rows, seen = [], set()
    for raw, encoding in candidates(data):
        url = redact_url(raw)
        if len(url) < 8 or url in seen:
            continue
        seen.add(url)
        try:
            domain = urlsplit(url).hostname or ""
        except ValueError:
            domain = ""
        rows.append({"app":app,"version":version,"url":url,"domain":domain.lower(),
          "category":classify_url(url),"source_file":str(path.relative_to(root)),
          "evidence_type":"static","extraction_method":method,
          "encoding":encoding,"confidence":"candidate"})
    return rows

def scan_tree(root: Path, app: str, version: str):
    rows = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rows.extend(scan_file(path, root, app, version))
    return rows
