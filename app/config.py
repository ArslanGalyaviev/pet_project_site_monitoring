import logging

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

logging.basicConfig(
    level=logging.INFO,
    filename="monitoring.log",
    format="%(asctime)s %(levelname)s %(message)s",
)

logging.getLogger("httpx").disabled = True
