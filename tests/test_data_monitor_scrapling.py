import types

from src.data.data_monitor import DataMonitor


def test_download_text_prefers_scrapling(monkeypatch):
    monitor = DataMonitor()

    def fake_scrapling_get(self, url):
        return "ok-from-scrapling"

    monkeypatch.setattr(DataMonitor, "_scrapling_get", fake_scrapling_get)

    assert monitor._download_text("https://example.com") == "ok-from-scrapling"


def test_download_text_falls_back_to_urllib(monkeypatch):
    monitor = DataMonitor()

    def fail_scrapling(self, url):
        raise RuntimeError("not installed")

    class DummyResp:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self):
            return b"ok-from-urllib"

    monkeypatch.setattr(DataMonitor, "_scrapling_get", fail_scrapling)
    monkeypatch.setattr("src.data.data_monitor.request.urlopen", lambda url, timeout: DummyResp())

    assert monitor._download_text("https://example.com") == "ok-from-urllib"


def test_extract_response_text_from_content_bytes():
    monitor = DataMonitor()
    response = types.SimpleNamespace(content=b"hello")

    assert monitor._extract_response_text(response) == "hello"
