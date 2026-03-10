from datetime import date
from unittest.mock import patch, Mock

import pytest

from lechuga.lechuga import Lechuga, _trend

TODAY = date.today().strftime("%Y-%m-%d")


class TestLechuga:
    def test_missing_api_key(self, monkeypatch, mock_db):
        monkeypatch.delenv("FIXERIOKEY", raising=False)
        with patch("lechuga.lechuga.requests.get"):
            with pytest.raises(Exception, match="FIXERIOKEY"):
                Lechuga()

    @patch("lechuga.lechuga.requests.get")
    def test_depth_1_calls_today(self, mock_get, mock_env, mock_db, mock_api_response):
        mock_get.return_value = Mock(
            json=Mock(return_value=mock_api_response(TODAY, 1.08, 1200.0))
        )

        client = Lechuga(depth=1)

        mock_get.assert_called_once()
        url = mock_get.call_args[0][0]
        assert TODAY in url
        assert "testkey123" in url
        assert len(client.p) == 1
        assert client.p[0]["date"] == TODAY
        assert client.p[0]["euro"] == 1200.0
        assert abs(client.p[0]["usd"] - 1200.0 / 1.08) < 0.01

    @patch("lechuga.lechuga.requests.get")
    def test_depth_3_sequential_dates(
        self, mock_get, mock_env, mock_db, mock_api_response
    ):
        mock_get.return_value = Mock()
        mock_get.return_value.json = Mock(
            side_effect=[
                mock_api_response(TODAY, 1.08, 1200.0),
                mock_api_response("2026-03-09", 1.07, 1190.0),
                mock_api_response("2026-03-08", 1.06, 1180.0),
            ]
        )

        client = Lechuga(depth=3)

        assert mock_get.call_count == 3
        urls = [call[0][0] for call in mock_get.call_args_list]
        assert TODAY in urls[0]
        assert "2026-03-09" in urls[1]
        assert "2026-03-08" in urls[2]
        assert len(client.p) == 3

    @patch("lechuga.lechuga.requests.get")
    def test_rate_calculation(self, mock_get, mock_env, mock_db, mock_api_response):
        mock_get.return_value = Mock(
            json=Mock(return_value=mock_api_response(TODAY, 1.08, 1200.0))
        )

        client = Lechuga(depth=1)

        entry = client.p[0]
        assert entry["euro"] == 1200.0
        assert abs(entry["usd"] - 1200.0 / 1.08) < 0.01

    @patch("lechuga.lechuga.requests.get")
    def test_depth_0_no_calls(self, mock_get, mock_env, mock_db):
        client = Lechuga(depth=0)

        mock_get.assert_not_called()
        assert client.p == []

    @patch("lechuga.lechuga.requests.get")
    def test_raise_for_status(self, mock_get, mock_env, mock_db):
        from requests.exceptions import HTTPError

        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError("500 Server Error")
        mock_get.return_value = mock_response

        with pytest.raises(HTTPError):
            Lechuga(depth=1)

    @patch("lechuga.lechuga.requests.get")
    def test_print_it_trend_emojis(
        self, mock_get, mock_env, mock_db, mock_api_response, capsys
    ):
        mock_get.return_value = Mock()
        mock_get.return_value.json = Mock(
            side_effect=[
                mock_api_response("2026-03-10", 1.08, 1200.0),
                mock_api_response("2026-03-09", 1.08, 1190.0),
                mock_api_response("2026-03-08", 1.08, 1100.0),
            ]
        )

        client = Lechuga(depth=3)
        client.print_it()
        output = capsys.readouterr().out

        # Row 1 (2026-03-08): oldest, no emoji
        # Row 2 (2026-03-09): 1190/1100 = +8.18% euro → 🚀
        assert "🚀" in output
        # Row 3 (2026-03-10): 1200/1190 = +0.84% euro → 📈
        assert "📈" in output

    def test_trend_helper(self):
        assert _trend(104, 100) == " 🚀"  # +4% > 3%
        assert _trend(102, 100) == " 📈"  # +2% ≤ 3%
        assert _trend(100, 100) == " ➡️"  # no change
        assert _trend(98, 100) == " 📉"  # -2% ≥ -3%
        assert _trend(96, 100) == " 💥"  # -4% < -3%
