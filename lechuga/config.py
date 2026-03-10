import os
import sqlite3
import requests_cache
from dotenv import load_dotenv
from colorama import init

load_dotenv()

SCRIPT_ROOT = os.path.dirname(os.path.realpath(__file__))
DB_PATH = os.path.join(SCRIPT_ROOT, "lechuga.sqlite")

init(autoreset=True)
requests_cache.install_cache(
    os.path.join(SCRIPT_ROOT, "lechuga"), backend="sqlite", expire_after=60
)


def get_db_connection(db_path=None):
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS rates (
            date TEXT PRIMARY KEY,
            usd REAL NOT NULL,
            euro REAL NOT NULL
        )
    """)
    conn.commit()
    return conn
