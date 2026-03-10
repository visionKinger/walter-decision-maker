import json

from src.reports import report_generator


class _FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps({"choices": [{"message": {"content": "ok"}}]}).encode("utf-8")


def test_generate_deepseek_report_uses_primary_key(monkeypatch):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "primary-key")
    monkeypatch.delenv("DEEKSEEK_API_KEY", raising=False)

    captured = {}

    def fake_urlopen(req, timeout=0):
        captured["auth"] = req.headers["Authorization"]
        return _FakeResponse()

    monkeypatch.setattr(report_generator.request, "urlopen", fake_urlopen)

    assert report_generator.generate_deepseek_report("ctx") == "ok"
    assert captured["auth"] == "Bearer primary-key"


def test_generate_deepseek_report_accepts_legacy_env_key(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.setenv("DEEKSEEK_API_KEY", "legacy-key")

    captured = {}

    def fake_urlopen(req, timeout=0):
        captured["auth"] = req.headers["Authorization"]
        return _FakeResponse()

    monkeypatch.setattr(report_generator.request, "urlopen", fake_urlopen)

    assert report_generator.generate_deepseek_report("ctx") == "ok"
    assert captured["auth"] == "Bearer legacy-key"


def test_build_fallback_report_is_plain_text():
    report = report_generator.build_fallback_report("sample context")

    assert "Executive Summary" in report
    assert "#" not in report
    assert "- [x]" not in report
