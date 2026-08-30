import asyncio
import httpx
import logging
from .models import Site
from .config import headers


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
