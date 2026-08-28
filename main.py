import asyncio
import httpx
import logging
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

logging.basicConfig(
    level=logging.INFO,
    filename="monitoring.log",
    format="%(asctime)s %(levelname)s %(message)s",
)

logging.getLogger("httpx").disabled = True


async def check_site(client, site):
    try:
        response = await client.get(site, timeout=5.0)
        return response
    except Exception as e:
        return e


async def check_sites(sites):
    async with httpx.AsyncClient(headers=headers) as client:
        tasks = [check_site(client, site) for site in sites]
        results = await asyncio.gather(*tasks)
        for ind, res in enumerate(results):
            if isinstance(res, Exception):
                logging.critical(f"{sites[ind]} - {str(res)}")
            else:
                match res.status_code // 100:
                    case 2:
                        logging.info(f"{sites[ind]} - Сайт доступен")
                    case 3:
                        logging.warning(f"{sites[ind]} - Переадресация")
                    case 4:
                        logging.error(f"{sites[ind]} - Ошибка клиента")
                    case 5:
                        logging.error(f"{sites[ind]} - Ошибка сайта")
                    case _:
                        logging.error(f"{sites[ind]} - Неизвестная ошибка")
    return results


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
    res = asyncio.run(check_sites(urls))
