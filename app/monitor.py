import asyncio
import httpx
import logging
from sqlmodel.ext.asyncio.session import AsyncSession
from .config import headers
from .models import Site
from .notifier import send_alert_email


async def check_site(
    client: httpx.AsyncClient, site: Site, session: AsyncSession
) -> None:
    while True:
        try:
            response = await client.get(site.url, timeout=site.timeout)
            is_failure = False
            error_msg = ""
            match response.status_code // 100:
                case 2:
                    logging.info(f"{site.url} - Сайт доступен")
                    site.record_success()
                case 3:
                    logging.warning(f"{site.url} - Переадресация")
                    site.record_success()
                case 4:
                    is_failure = True
                    error_msg = f"Ошибка клиента (статус {response.status_code})"
                case 5:
                    is_failure = True
                    error_msg = f"Ошибка сервера (статус {response.status_code})"
                case _:
                    is_failure = True
                    error_msg = f"Неизвестный статус {response.status_code}"
            if is_failure:
                logging.error(f"{site.url} - {error_msg}")
                if site.record_failure():
                    session.add(site)
                    await session.commit()
                    await send_alert_email(site.url, error_msg)
        except Exception as e:
            error_msg = str(e)
            logging.critical(f"Произошла ошибка {error_msg} при запросе к {site.url}")
            if site.record_failure():
                session.add(site)
                await session.commit()
                await send_alert_email(site.url, error_msg)

        await asyncio.sleep(site.check_interval)


async def check_sites(sites: dict[str, Site], session: AsyncSession):
    async with httpx.AsyncClient(headers=headers) as client:
        tasks = [check_site(client, site, session) for site in sites.values()]
        await asyncio.gather(*tasks)
