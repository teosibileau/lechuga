import pytest


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("FIXERIOKEY", "testkey123")


def _make_response(date, usd_rate, ars_rate):
    return {
        "success": True,
        "date": date,
        "rates": {"USD": usd_rate, "ARS": ars_rate},
    }


@pytest.fixture
def mock_api_response():
    return _make_response
