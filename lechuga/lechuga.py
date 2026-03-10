import click
from datetime import date, datetime, timedelta
import os
import logging
import requests
from colorama import Fore, Back, Style
from tabulate import tabulate

from lechuga.config import get_db_connection
from lechuga.models import Rate, cached_rate


def _trend(current, previous):
    pct = (current - previous) / previous * 100
    if pct > 3:
        return " 🚀"
    if pct > 0:
        return " 📈"
    if pct < -3:
        return " 💥"
    if pct < 0:
        return " 📉"
    return " ➡️"


class Lechuga:
    def __init__(self, depth=1):
        self.api_key = os.environ.get("FIXERIOKEY", False)
        if not self.api_key:
            raise Exception("Please set the FIXERIOKEY environ variable")
        self.depth = depth
        self.p = []
        self.db_conn = get_db_connection()
        self.refresh()

    @cached_rate
    def fetch_rate(self, date_str):
        API = "http://data.fixer.io/api/%s?access_key=%s&format=1&symbols=USD,ARS"
        uri = API % (date_str, self.api_key)
        r = requests.get(uri)
        r.raise_for_status()
        r = r.json()
        return Rate(
            date=r["date"],
            usd=r["rates"]["ARS"] / r["rates"]["USD"],
            euro=r["rates"]["ARS"],
        )

    def refresh(self):
        last = False
        while self.depth:
            date_str = (
                date.today().strftime("%Y-%m-%d")
                if not last
                else last.strftime("%Y-%m-%d")
            )
            rate = self.fetch_rate(date_str)
            self.p.append(rate.model_dump())
            last = datetime.strptime(rate.date, "%Y-%m-%d") - timedelta(days=1)
            self.depth -= 1

    def print_it(self):
        print("")
        h = [
            Back.YELLOW + Fore.BLACK + " Fecha " + Style.RESET_ALL,
            Back.GREEN + Fore.WHITE + " USD " + Style.RESET_ALL,
            Back.BLUE + Fore.WHITE + " EURO " + Style.RESET_ALL,
        ]
        rows = list(reversed(self.p))
        o = []
        for idx, i in enumerate(rows):
            usd_str = "%.2f" % i["usd"]
            euro_str = "%.2f" % i["euro"]
            if idx > 0:
                usd_str += _trend(i["usd"], rows[idx - 1]["usd"])
                euro_str += _trend(i["euro"], rows[idx - 1]["euro"])
            o.append([i["date"], usd_str, euro_str])
        print(tabulate(o, headers=h))
        print("")


@click.command()
@click.option("--n", default=4, help="How far in the past should we go?")
def run(n):
    client = Lechuga(n)
    client.print_it()


if __name__ == "__main__":
    logging.captureWarnings(True)
    run()
