import functools

from pydantic import BaseModel


class Rate(BaseModel):
    date: str
    usd: float
    euro: float


def cached_rate(fn):
    @functools.wraps(fn)
    def wrapper(self, date_str):
        row = self.db_conn.execute(
            "SELECT date, usd, euro FROM rates WHERE date = ?", (date_str,)
        ).fetchone()
        if row:
            return Rate(date=row[0], usd=row[1], euro=row[2])

        rate = fn(self, date_str)

        self.db_conn.execute(
            "INSERT OR IGNORE INTO rates (date, usd, euro) VALUES (?, ?, ?)",
            (rate.date, rate.usd, rate.euro),
        )
        self.db_conn.commit()
        return rate

    return wrapper
