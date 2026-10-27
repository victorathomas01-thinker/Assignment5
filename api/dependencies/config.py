"""Application settings. Keep passwords outside Git."""
import os


class conf:
    host = os.getenv("MYSQL_HOST", "localhost")
    database = os.getenv("MYSQL_DATABASE", "sandwich_maker_api")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    user = os.getenv("MYSQL_USER", "root")
    password = os.getenv("MYSQL_PASSWORD", "")
