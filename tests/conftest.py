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


@pytest.fixture
def mock_db(tmp_path, monkeypatch):
    """Patch get_db_connection to use a temp DB."""
    db_path = str(tmp_path / "test.sqlite")
    import lechuga.config as config

    monkeypatch.setattr(config, "DB_PATH", db_path)
    return db_path
