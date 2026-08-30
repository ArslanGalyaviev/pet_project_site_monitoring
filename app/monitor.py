import asyncio
import httpx
import logging
from .config import headers
from .models import Site


async def check_site(client, site, session):
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
                    if site.record_failure():
                        session.add(site)
                        await session.commit()
                case 5:
                    logging.error(f"{site.url} - Ошибка сайта")
                    if site.record_failure():
                        session.add(site)
                        await session.commit()
                case _:
                    logging.error(f"{site.url} - Неизвестная ошибка")
                    if site.record_failure():
                        session.add(site)
                        await session.commit()
        except Exception as e:
            logging.critical(f"Произошла ошибка {e} при запросе к {site.url}")
            if site.record_failure():
                session.add(site)
                await session.commit()
        await asyncio.sleep(site.check_interval)


async def check_sites(sites, session):
    async with httpx.AsyncClient(headers=headers) as client:
        tasks = [check_site(client, site, session) for site in sites.values()]
        await asyncio.gather(*tasks)
