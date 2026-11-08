from url_atlas.extract import classify_url, redact_url, scan_file

def test_secret_query_is_redacted():
    assert "access_token=[REDACTED]" in redact_url("https://example.com/api?access_token=abc&view=full")

def test_classification():
    assert classify_url("wss://example.com/socket") == "websocket"
    assert classify_url("https://example.com/v1/models") == "api"

def test_binary_scan(tmp_path):
    p=tmp_path/"classes.dex"; p.write_bytes(b"x https://api.example.com/v1/models y")
    rows=scan_file(p,tmp_path,"chatgpt","1.0")
    assert any(r["url"].startswith("https://api.example.com") for r in rows)
