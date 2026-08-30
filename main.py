import asyncio
from app.monitor import check_sites
from app.models import Site
from app.database import init_db
from app.database import DATABASE_URL
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.ext.asyncio import create_async_engine


async def main():
    engine = create_async_engine(DATABASE_URL, echo=True)
    await init_db(engine)
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
    async with AsyncSession(engine, expire_on_commit=False) as session:
        resp = await session.exec(select(Site))
        if not resp.all():
            for u in urls:
                site_object = Site(url=u, check_interval=5, timeout=5)
                session.add(site_object)
            await session.commit()
        sites_from_db = await session.exec(select(Site))
        sites = {site.url: site for site in sites_from_db.all()}
        await check_sites(sites, session)


if __name__ == "__main__":
    asyncio.run(main())
