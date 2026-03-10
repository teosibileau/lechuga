from unittest.mock import Mock

from lechuga.config import get_db_connection
from lechuga.models import Rate, cached_rate


class FakeService:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    @cached_rate
    def fetch(self, date_str):
        pass


class TestCachedRate:
    def test_cache_miss_calls_fn_and_stores(self, mock_db):
        conn = get_db_connection()
        svc = FakeService(conn)
        expected = Rate(date="2026-01-15", usd=1111.11, euro=1200.0)
        svc.fetch = cached_rate(Mock(return_value=expected))
        # Bind self manually since we replaced the method
        result = svc.fetch(svc, "2026-01-15")

        svc.fetch.__wrapped__.assert_called_once_with(svc, "2026-01-15")
        assert result == expected

        row = conn.execute(
            "SELECT date, usd, euro FROM rates WHERE date = ?", ("2026-01-15",)
        ).fetchone()
        assert row is not None
        assert row[0] == "2026-01-15"
        assert row[1] == 1111.11
        assert row[2] == 1200.0
        conn.close()

    def test_cache_hit_skips_fn(self, mock_db):
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO rates (date, usd, euro) VALUES (?, ?, ?)",
            ("2026-01-15", 1111.11, 1200.0),
        )
        conn.commit()

        svc = FakeService(conn)
        inner = Mock()
        svc.fetch = cached_rate(inner)

        result = svc.fetch(svc, "2026-01-15")

        inner.assert_not_called()
        assert result == Rate(date="2026-01-15", usd=1111.11, euro=1200.0)
        conn.close()

    def test_duplicate_insert_ignored(self, mock_db):
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO rates (date, usd, euro) VALUES (?, ?, ?)",
            ("2026-01-15", 1111.11, 1200.0),
        )
        conn.commit()

        svc = FakeService(conn)
        # Inner fn returns a Rate whose date collides with existing row
        colliding = Rate(date="2026-01-15", usd=9999.99, euro=8888.88)
        svc.fetch = cached_rate(Mock(return_value=colliding))

        # Fetch a different date so cache misses, but returned Rate's date collides
        result = svc.fetch(svc, "2026-01-20")
        assert result == colliding  # no error raised
        conn.close()
