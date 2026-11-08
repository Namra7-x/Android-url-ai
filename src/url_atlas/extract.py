from __future__ import annotations

import ipaddress
import io
import re
import zipfile
from pathlib import Path
from urllib.parse import unquote_plus, urlsplit, urlunsplit

# URLs are extracted from printable strings, decoded text pools, and every
# decompressed APK entry. The character cap avoids runaway matches in binaries.
MAX_URL_LENGTH = 4096
URL_RE = re.compile(
    rb"(?i)(?<![a-z0-9+.-])(?:https?|wss?|ftp)://"
    rb"[^\x00-\x20\x7f\"'<>\\{}\[\]]{1,4096}"
)
CUSTOM_RE = re.compile(
    rb"(?i)(?<![a-z0-9+.-])[a-z][a-z0-9+.-]{1,30}://"
    rb"[^\x00-\x20\x7f\"'<>\\{}\[\]]{1,2048}"
)
SINGLE_SCHEME_RE = re.compile(
    rb"(?i)(?<![a-z0-9+.-])(?:mailto|tel|sms):"
    rb"[^\x00-\x20\x7f\"'<>\\{}\[\]]{1,1024}"
)

# Deliberately use known public and common private suffixes here. A catch-all
# [a-z]{2,63} suffix turns Java/Kotlin namespaces into fake domains.
DOMAIN_SUFFIXES = (
    b"com|net|org|edu|gov|mil|int|io|ai|app|dev|co|uk|in|us|ca|de|fr|jp|au|"
    b"google|googleapis|me|xyz|tech|info|biz|tv|gg|so|cloud|site|online|store|"
    b"tools|systems|digital|technology|services|support|media|live|space|email|"
    b"world|one|pro|mobi|travel|agency|company|today|news|social|network|"
    b"solutions|website|group|team|works|finance|health|wiki|design|software|"
    b"corp|internal|local|test"
)
DOMAIN_RE = re.compile(
    rb"(?i)(?<![a-z0-9_.:/-])"
    rb"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+"
    rb"(?:"
    + DOMAIN_SUFFIXES
    + rb")(?![a-z0-9-])(?::[0-9]{1,5})?"
    rb"(?:[/?#][^\s\x00\"'<>\\{}\[\]]{0,1024})?"
)

SECRET_KEYS = {
    "token", "access_token", "refresh_token", "id_token", "api_key", "apikey",
    "key", "authorization", "auth", "signature", "sig", "password", "passwd",
    "code", "session", "sessionid", "client_secret", "secret", "credential",
    "credentials",
}
SECRET_NORMALISED = {re.sub(r"[^a-z0-9]", "", key) for key in SECRET_KEYS}
PACKAGE_PREFIXES = {
    "com", "org", "net", "io", "android", "androidx", "java", "javax",
    "kotlin", "dalvik", "sun", "gnu",
}
STANDARD_SCHEMES = {"http", "https", "ws", "wss", "ftp"}
PLATFORM_SCHEMES = {"file", "content", "android.resource", "resource"}


def _unescape_literal(value: str) -> str:
    """Undo common JSON/Java URL escapes without decoding percent-encoded paths."""
    value = value.replace(r"\/", "/")
    value = re.sub(
        r"\\u([0-9a-fA-F]{4})",
        lambda match: chr(int(match.group(1), 16)),
        value,
    )
    value = re.sub(
        r"\\x([0-9a-fA-F]{2})",
        lambda match: chr(int(match.group(1), 16)),
        value,
    )
    return value


def _trim_candidate(value: str) -> str:
    value = _unescape_literal(value.strip().strip("\"'<>"))
    # Strip punctuation commonly attached by source-code and prose delimiters.
    while value and value[-1] in ".,;!":
        value = value[:-1]
    # Keep balanced parentheses/brackets in URLs, but remove unmatched closers.
    for closing, opening in ((")", "("), ("]", "["), ("}", "{")):
        while value.endswith(closing) and value.count(closing) > value.count(opening):
            value = value[:-1]
    return value


def _is_secret_key(key: str) -> bool:
    normalised = re.sub(r"[^a-z0-9]", "", unquote_plus(key).lower())
    if normalised in SECRET_NORMALISED:
        return True
    return any(
        normalised.endswith(suffix)
        for suffix in ("accesstoken", "refreshtoken", "apikey", "clientsecret")
    )


def _redact_params(value: str) -> str:
    parts = []
    for item in value.split("&") if value else []:
        key, separator, content = item.partition("=")
        if separator and _is_secret_key(key):
            content = "[REDACTED]"
        parts.append(key + (separator + content if separator else ""))
    return "&".join(parts)


def redact_url(value: str) -> str:
    """Normalise URL casing and redact sensitive query/fragment parameters."""
    value = _trim_candidate(value)
    try:
        parsed = urlsplit(value)
        if not parsed.scheme:
            path, marker, query = value.partition("?")
            if marker:
                query, hash_marker, fragment = query.partition("#")
                result = path + "?" + _redact_params(query)
                if hash_marker:
                    result += "#" + _redact_params(fragment)
                return result
            return value

        query = _redact_params(parsed.query)
        fragment = _redact_params(parsed.fragment) if "=" in parsed.fragment else parsed.fragment
        scheme = parsed.scheme.lower()
        if parsed.hostname:
            host = parsed.hostname.encode("idna").decode("ascii").lower()
            if ":" in host and not host.startswith("["):
                host = f"[{host}]"
            port = parsed.port
            netloc = host + (f":{port}" if port is not None else "")
        else:
            netloc = parsed.netloc.lower()
        return urlunsplit((scheme, netloc, parsed.path, query, fragment))
    except (UnicodeError, ValueError):
        return value


def _valid_hostname(host: str, *, require_dot: bool = False) -> bool:
    if not host or len(host) > 253 or any(ch.isspace() for ch in host):
        return False
    host = host.rstrip(".")
    try:
        ipaddress.ip_address(host)
        return not require_dot
    except ValueError:
        pass
    if host.lower() == "localhost":
        return not require_dot
    labels = host.split(".")
    if require_dot and len(labels) < 2:
        return False
    return all(
        0 < len(label) <= 63
        and re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?", label)
        for label in labels
    )


def _normalise_candidate(raw: str):
    value = _trim_candidate(raw)
    if not value or len(value) > MAX_URL_LENGTH:
        return None

    try:
        parsed = urlsplit(value)
    except ValueError:
        return None

    scheme = parsed.scheme.lower()
    if scheme in STANDARD_SCHEMES:
        try:
            host = parsed.hostname
            port = parsed.port
        except ValueError:
            return None
        if not host or not _valid_hostname(host):
            return None
        normalised = redact_url(value)
        try:
            clean = urlsplit(normalised)
            domain = clean.hostname or ""
        except ValueError:
            return None
        if not clean.netloc or not domain:
            return None
        return normalised, classify_url(normalised), domain.lower()

    if scheme:
        if scheme in {"javascript", "data"}:
            return None
        if not parsed.netloc and not parsed.path:
            return None
        normalised = redact_url(value)
        category = "platform-uri" if scheme in PLATFORM_SCHEMES else "custom-uri"
        host = ""
        try:
            host = urlsplit(normalised).hostname or ""
        except ValueError:
            pass
        return normalised, category, host.lower()

    # A scheme-less host/path is retained as a domain reference, not mislabeled
    # as a custom deep link and not silently promoted to an https:// URL.
    try:
        domain_parts = urlsplit("//" + value)
        host = domain_parts.hostname or ""
        _ = domain_parts.port
    except ValueError:
        return None
    if not _valid_hostname(host, require_dot=True):
        return None
    labels = host.lower().split(".")
    if labels[0] in PACKAGE_PREFIXES:
        return None
    # DOMAIN_RE already restricts suffixes; this check also protects callers
    # that invoke this normaliser directly.
    if not re.search(r"\.(" + DOMAIN_SUFFIXES.decode("ascii") + r")$", host, re.I):
        return None
    normalised = redact_url(value)
    return normalised, "domain-reference", host.lower()


def candidates(data: bytes):
    """Yield raw URL/domain strings and the encoding used to find them."""
    # Common escaped JSON/Java string representations.
    searchable = re.sub(rb"\\u003[aA]", b":", data, flags=re.I)
    searchable = re.sub(rb"\\u002[fF]", b"/", searchable, flags=re.I)
    searchable = re.sub(rb"\\u0026", b"&", searchable, flags=re.I)
    searchable = searchable.replace(b"\\/", b"/")

    for pattern, label in (
        (URL_RE, "bytes-ascii"),
        (CUSTOM_RE, "bytes-custom-uri"),
        (SINGLE_SCHEME_RE, "bytes-single-scheme"),
        (DOMAIN_RE, "bytes-domain"),
    ):
        for match in pattern.finditer(searchable):
            yield match.group(0).decode("utf-8", "replace"), label

    # Wide strings occur in native ELF data and resource payloads. Avoid
    # interpreting every arbitrary binary file as UTF-16 unless NUL bytes exist.
    if searchable and searchable.count(b"\x00") / len(searchable) >= 0.02:
        for encoding in ("utf-16le", "utf-16be"):
            text = searchable.decode(encoding, "ignore")
            if not text:
                continue
            encoded = text.encode("utf-8", "ignore")
            for pattern, label in (
                (URL_RE, encoding),
                (CUSTOM_RE, encoding),
                (SINGLE_SCHEME_RE, encoding),
                (DOMAIN_RE, encoding),
            ):
                for match in pattern.finditer(encoded):
                    yield match.group(0).decode("utf-8", "replace"), label


def scan_bytes(
    data: bytes,
    source_file: str,
    app: str,
    version: str,
    method: str = "raw-byte-scan",
):
    rows = {}
    for raw, encoding in candidates(data):
        result = _normalise_candidate(raw)
        if result is None:
            continue
        url, category, domain = result
        key = (url, category)
        if key in rows:
            continue
        rows[key] = {
            "app": app,
            "version": version,
            "url": url,
            "domain": domain,
            "category": category,
            "source_file": source_file,
            "evidence_type": "static",
            "extraction_method": method,
            "encoding": encoding,
            "confidence": "candidate",
        }
    return list(rows.values())


def scan_file(path: Path, root: Path, app: str, version: str, method="raw-byte-scan"):
    try:
        data = path.read_bytes()
    except OSError:
        return []
    return scan_bytes(data, str(path.relative_to(root)), app, version, method)


def _scan_archive_payload(
    data: bytes,
    source_file: str,
    app: str,
    version: str,
    depth: int = 0,
):
    rows = scan_bytes(data, source_file, app, version, "apk-entry-scan")
    if depth >= 2 or not data.startswith(b"PK"):
        return rows
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            for info in sorted(archive.infolist(), key=lambda item: item.filename):
                if info.is_dir():
                    continue
                try:
                    child = archive.read(info)
                except (OSError, RuntimeError, zipfile.BadZipFile):
                    continue
                child_source = f"{source_file}!/{info.filename}"
                rows.extend(_scan_archive_payload(child, child_source, app, version, depth + 1))
    except (OSError, zipfile.BadZipFile):
        pass
    return rows


def scan_apk(path: Path, root: Path, app: str, version: str):
    """Scan the APK container and every decompressed entry in every APK split."""
    try:
        container_rows = scan_file(path, root, app, version, "apk-container-byte-scan")
    except OSError:
        container_rows = []
    rows = list(container_rows)
    try:
        with zipfile.ZipFile(path) as archive:
            for info in sorted(archive.infolist(), key=lambda item: item.filename):
                if info.is_dir():
                    continue
                try:
                    data = archive.read(info)
                except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
                    print(f"[WARN] {path.name}!/{info.filename}: {exc}")
                    continue
                source_file = f"{path.relative_to(root)}!/{info.filename}"
                rows.extend(_scan_archive_payload(data, source_file, app, version))
    except (OSError, zipfile.BadZipFile) as exc:
        print(f"[WARN] Could not inspect APK archive {path}: {exc}")
    return rows


def classify_url(url: str) -> str:
    try:
        parsed = urlsplit(url)
    except ValueError:
        return "domain-reference" if "://" not in url else "custom-uri"
    scheme = parsed.scheme.lower()
    if scheme in {"ws", "wss"}:
        return "websocket"
    if scheme in {"http", "https", "ftp"}:
        path = parsed.path.lower()
        if any(token in path for token in ("/graphql", "/api/", "/v1/", "/v2/", "/rpc", "/rest/")):
            return "api"
        host = (parsed.hostname or "").lower()
        if any(token in host for token in ("cdn", "static", "assets", "gstatic")):
            return "asset-or-cdn"
        return "http-url"
    if scheme in PLATFORM_SCHEMES:
        return "platform-uri"
    return "custom-uri"


def scan_tree(root: Path, app: str, version: str):
    rows = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        rows.extend(scan_file(path, root, app, version))
    return rows
