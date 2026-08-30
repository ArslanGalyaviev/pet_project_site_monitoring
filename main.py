import asyncio
from app.monitor import check_sites
from app.models import Site

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
