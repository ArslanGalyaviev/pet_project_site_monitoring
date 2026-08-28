import requests
import httpx
import asyncio
import time

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def using_requests(urls):
    start_time = time.perf_counter()
    with requests.session() as session:
        session.headers.update(headers)
        for u in urls:
            try:
                session.get(u, timeout=5.0)
            except Exception:
                pass
    time_spent = time.perf_counter() - start_time
    return time_spent


def using_httpx(urls):
    start_time = time.perf_counter()
    with httpx.Client(headers=headers) as client:
        for u in urls:
            try:
                client.get(u, timeout=5.0)
            except Exception:
                pass
    time_spent = time.perf_counter() - start_time
    return time_spent


async def using_async_httpx(urls):
    start_time = time.perf_counter()
    async with httpx.AsyncClient(headers=headers) as client:
        tasks = [client.get(u, timeout=5.0) for u in urls]
        await asyncio.gather(*tasks, return_exceptions=True)
    time_spent = time.perf_counter() - start_time
    return time_spent


def benchmark(urls, repetitions=5):
    results = []
    for name, func in [
        ("requests", using_requests),
        ("синхронный httpx", using_httpx),
        ("асинхронный httpx", using_async_httpx),
    ]:
        times = []
        for _ in range(repetitions):
            if "асинхронный" in name:
                t = asyncio.run(func(urls))
            else:
                t = func(urls)
            times.append(t)
        results.append((name, min(times), max(times), sum(times) / repetitions))
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
    benchmark_results = benchmark(urls)
    output = []
    output.append(
        f"{'Метод':^20} | {'Мин. время':^12} | {'Макс. время':^12} | {'Сред. время':^12}"
    )
    output.append("-" * 64)
    for r in benchmark_results:
        output.append(
            " | ".join(
                (f"{v:^12.3f}" if i > 0 else f"{v:^20}" for i, v in enumerate(r))
            )
        )
    with open("benchmark_results.txt", "w", encoding="utf-8") as f:
        for row in output:
            f.write(row + "\n")
