from url_atlas.extract import (
    candidates, classify_url, redact_url, scan_apk, scan_bytes, scan_file,
)


def test_secret_query_is_redacted():
    value = redact_url("https://example.com/api?access_token=abc&view=full")
    assert "access_token=[REDACTED]" in value
    assert "view=full" in value


def test_secret_fragment_is_redacted():
    value = redact_url("https://example.com/#token=abc&tab=home")
    assert "token=[REDACTED]" in value
    assert "tab=home" in value


def test_classification():
    assert classify_url("wss://example.com/socket") == "websocket"
    assert classify_url("https://example.com/v1/models") == "api"
    assert classify_url("content://com.example.provider/items") == "platform-uri"


def test_binary_scan(tmp_path):
    path = tmp_path / "classes.dex"
    path.write_bytes(b"x https://api.example.com/v1/models y")
    rows = scan_file(path, tmp_path, "chatgpt", "1.0")
    assert any(row["url"].startswith("https://api.example.com") for row in rows)


def test_does_not_mislabel_package_names_as_domains():
    data = (
        b"com.google.android.gms.common "
        b"androidx.lifecycle.ViewModelProvider "
        b"org.jetbrains.kotlin "
        b"https://api.example.com/v1/models"
    )
    rows = scan_bytes(data, "classes.dex", "chatgpt", "1.0")
    values = {row["url"] for row in rows}
    assert "https://api.example.com/v1/models" in values
    assert "com.google.android.gms.common" not in values
    assert "androidx.lifecycle.ViewModelProvider" not in values
    assert "org.jetbrains.kotlin" not in values


def test_domain_references_are_separate_candidates():
    rows = scan_bytes(
        b"api.example.com and https://api.example.com/v1",
        "classes.dex", "chatgpt", "1.0",
    )
    categories = {(row["url"], row["category"]) for row in rows}
    assert ("api.example.com", "domain-reference") in categories
    assert ("https://api.example.com/v1", "api") in categories


def test_escaped_json_urls_are_found():
    rows = scan_bytes(
        br'{"endpoint":"https:\\/\\/api.example.com\\/v1?access_token=abc"}',
        "assets/config.json", "chatgpt", "1.0",
    )
    assert any(
        row["url"].startswith("https://api.example.com/v1")
        and "[REDACTED]" in row["url"]
        for row in rows
    )


def test_utf16le_urls_are_found():
    data = "https://wide.example.com/v2/items".encode("utf-16le")
    rows = scan_bytes(data, "libsample.so", "chatgpt", "1.0")
    assert any(row["url"].startswith("https://wide.example.com") for row in rows)


def test_scan_apk_decompresses_all_entries(tmp_path):
    import zipfile

    apk_root = tmp_path / "input"
    apk_root.mkdir()
    apk = apk_root / "base.apk"
    with zipfile.ZipFile(apk, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr(
            "classes.dex",
            b"not-a-real-dex https://dex.example.com/v1/endpoint",
        )
        archive.writestr(
            "assets/settings.json",
            b'{"host":"https://asset.example.net/config"}',
        )
        archive.writestr(
            "lib/arm64-v8a/libnetwork.so",
            b"native https://native.example.org/connect",
        )

    rows = scan_apk(apk, apk_root, "chatgpt", "1.0")
    found = {row["url"] for row in rows}
    assert "https://dex.example.com/v1/endpoint" in found
    assert "https://asset.example.net/config" in found
    assert "https://native.example.org/connect" in found
    assert any("classes.dex" in row["source_file"] for row in rows)
    assert any("assets/settings.json" in row["source_file"] for row in rows)
    assert any("libnetwork.so" in row["source_file"] for row in rows)



def test_rejects_scheme_prefixes_glued_to_standard_urls():
    data = (
        b"ahttps://api.example.com/v1 "
        b"bhttps://cdn.example.com/image.png "
        b"cfile:/android_asset/index.html "
        b"codexmlhttp://www.w3.org/2000/xmlns/ "
        b"https://valid.example.com/path "
        b"chatgpt://codex"
    )
    rows = scan_bytes(data, "classes.dex", "chatgpt", "1.0")
    urls = {row["url"] for row in rows}
    assert "https://valid.example.com/path" in urls
    assert "chatgpt://codex" in urls
    assert not any(url.startswith(("ahttps://", "bhttps://")) for url in urls)
    assert "cfile:/android_asset/index.html" not in urls
    assert "codexmlhttp://www.w3.org/2000/xmlns/" not in urls
