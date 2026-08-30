import asyncio
import httpx
import logging

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

logging.basicConfig(
    level=logging.INFO,
    filename="monitoring.log",
    format="%(asctime)s %(levelname)s %(message)s",
)

logging.getLogger("httpx").disabled = True


class Site:
    def __init__(
        self,
        url,
        timeout=5.0,
        check_interval=60,
        consecutive_errors=0,
        alert_sent=False,
    ):
        self.url = url
        self.timeout = timeout
        self.check_interval = check_interval
        self.consecutive_errors = consecutive_errors
        self.alert_sent = alert_sent

    def record_success(self):
        self.consecutive_errors = 0
        self.alert_sent = False

    def record_failure(self):
        self.consecutive_errors += 1
        if self.consecutive_errors >= 5 and not self.alert_sent:
            logging.critical(f"Сайт {self.url} долго не работает")
            self.alert_sent = True


async def check_site(client, site):
    while True:
        try:
            response = await client.get(site.url, timeout=site.timeout)
            match response.status_code // 100:
                case 2:
                    logging.info(f"{site.url} - Сайт доступен")
                    site.record_success()
                case 3:
                    logging.warning(f"{site.url} - Переадресация")
                    site.record_success()
                case 4:
                    logging.error(f"{site.url} - Ошибка клиента")
                    site.record_failure()
                case 5:
                    logging.error(f"{site.url} - Ошибка сайта")
                    site.record_failure()
                case _:
                    logging.error(f"{site.url} - Неизвестная ошибка")
                    site.record_failure()
        except Exception as e:
            logging.critical(f"Произошла ошибка {e} при запросе к {site.url}")
            site.record_failure()
        await asyncio.sleep(site.check_interval)


async def check_sites(sites):
    async with httpx.AsyncClient(headers=headers) as client:
        tasks = [check_site(client, site) for site in sites.values()]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    urls = [
        "https://postman-echo.com/get",
        "https://reqres.in/api/users/1",
        "https://icanhazip.com",
        "https://ifconfig.me",
        "https://mockbin.org/request",
        "https://httpbingo.org/get",
        "https://google.com",
        "https://yandex.ru",
    ]
    sites = {url: Site(url, check_interval=5) for url in urls}
    res = asyncio.run(check_sites(sites))
